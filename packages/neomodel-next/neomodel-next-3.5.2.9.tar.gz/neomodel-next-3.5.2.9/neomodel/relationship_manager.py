import sys
import functools
from importlib import import_module
from .exceptions import NotConnected
from .util import deprecated, _get_node_properties
from .match import OUTGOING, INCOMING, EITHER, _rel_helper, Traversal, NodeSet, process_filter_args
from .relationship import StructuredRel
from .match import TraversalRelationships, _UNARY_OPERATORS
from .match_q import QBase, Q
from .core import StructuredNode, db


# basestring python 3.x fallback
try:
    basestring
except NameError:
    basestring = str


# check source node is saved and not deleted
def check_source(fn):
    fn_name = fn.func_name if hasattr(fn, 'func_name') else fn.__name__

    @functools.wraps(fn)
    def checker(self, *args, **kwargs):
        self.source._pre_action_check(self.name + '.' + fn_name)
        return fn(self, *args, **kwargs)
    return checker


class RelationshipManager(object):
    """
    Base class for all relationships managed through neomodel.

    I.e the 'friends' object in  `user.friends.all()`
    """

    def __init__(self, source, key, definition):
        self.source = source
        self.source_class = source.__class__
        self.name = key
        self.definition = definition
        self._place_holder_registry = {}
        self._query_params = {}

    def __str__(self):
        direction = 'either'
        if self.definition['direction'] == OUTGOING:
            direction = 'a outgoing'
        elif self.definition['direction'] == INCOMING:
            direction = 'a incoming'

        return "{0} in {1} direction of type {2} on node ({3}) of class '{4}'".format(
            self.description, direction,
            self.definition['relation_type'], self.source.id, self.source_class.__name__)

    def _check_node(self, obj):
        """check for valid node i.e correct class and is saved"""
        if not issubclass(type(obj), self.definition['node_class']):
            raise ValueError("Expected node of class " + self.definition['node_class'].__name__)
        if not hasattr(obj, 'id'):
            raise ValueError("Can't perform operation on unsaved node " + repr(obj))

    def _check_nodeset(self, obj):
        """check for valid nodeset i.e correct class and is saved"""
        if not issubclass(obj.source, self.definition['node_class']):
            raise ValueError("Expected node of class " + self.definition['node_class'].__name__)

    @check_source
    def connect(self, node, properties=None):
        """
        Connect a node

        :param node:
        :param properties: for the new relationship
        :type: dict
        :return:
        """
        self._check_node(node)

        if not self.definition['model'] and properties:
            raise NotImplementedError(
                "Relationship properties without using a relationship model "
                "is no longer supported."
            )

        params = {}
        rel_model = self.definition['model']
        rp = None  # rel_properties

        if rel_model:
            rp = {}
            # need to generate defaults etc to create fake instance
            tmp = rel_model(**properties) if properties else rel_model()
            # build params and place holders to pass to rel_helper
            for p, v in rel_model.deflate(tmp.__properties__).items():
                rp[p] = '{' + p + '}'
                params[p] = v

            # set right_id and left_id
            tmp.start_node_id = self.source.id,
            tmp.end_node_id = node.id

            if hasattr(tmp, 'pre_save'):
                tmp.pre_save()

        new_rel = _rel_helper(lhs='us', rhs='them', ident='r',
                              relation_properties=rp, **self.definition)
        q = "MATCH (them), (us) WHERE id(them)={them} and id(us)={self} " \
            "CREATE UNIQUE" + new_rel

        params['them'] = node.id

        if not rel_model:
            self.source.cypher(q, params)
            return True

        rel_ = self.source.cypher(q + " RETURN r", params)[0][0][0]
        rel_instance = self._set_start_end_cls(rel_model.inflate(rel_), node)

        if hasattr(rel_instance, 'post_save'):
            rel_instance.post_save()

        return rel_instance

    @check_source
    def connect_nodeset(self, nodeset, properties=None, inflate_rels=True):
        self._check_nodeset(nodeset)

        if not self.definition['model'] and properties:
            raise NotImplementedError(
                "Relationship properties without using a relationship model "
                "is no longer supported."
            )

        params = {}
        rel_model = self.definition['model']
        rp = None  # rel_properties

        if rel_model:
            rp = {}
            # need to generate defaults etc to create fake instance
            tmp = rel_model(**properties) if properties else rel_model()
            # build params and place holders to pass to rel_helper
            for p, v in rel_model.deflate(tmp.__properties__).items():
                rp[p] = '{' + p + '}'
                params[p] = v

            if hasattr(tmp, 'pre_save'):
                tmp.pre_save()

        new_rel = _rel_helper(lhs='us', rhs=nodeset.ident, ident='r',
                              relation_properties=rp, **self.definition)

        qb = nodeset.query_builder
        nodeset_query = qb.build_query(return_operation="WITH")
        nodeset_params = qb._query_params

        q = nodeset_query + " MATCH ({})".format(nodeset.ident) + \
            ", (us) WHERE id(us)={self} CREATE UNIQUE" + new_rel

        # update the nodeset params
        params.update(nodeset_params)

        if not rel_model:
            self.source.cypher(q, params)
            return True

        rels_ = self.source.cypher(q + " RETURN r", params)
        if rels_ and rels_[0]:
            rels_ = rels_[0][0]
        else:
            return []

        if inflate_rels:
            rel_instance = [
                self._set_start_end_cls(
                    rel_model.inflate(rel_),
                    nodeset.source) for rel_ in rels_]

            if hasattr(rel_instance, 'post_save'):
                rel_instance.post_save()

            return rel_instance
        return True

    @check_source
    def replace(self, node, properties=None):
        """
        Disconnect all existing nodes and connect the supplied node

        :param node:
        :param properties: for the new relationship
        :type: dict
        :return:
        """
        self.disconnect_all()
        self.connect(node, properties)

    @check_source
    def relationship(self, node):
        """
        Retrieve the relationship object for this first relationship between self and node.

        :param node:
        :return: StructuredRel
        """
        self._check_node(node)
        my_rel = _rel_helper(lhs='us', rhs='them', ident='r', **self.definition)
        q = "MATCH " + my_rel + " WHERE id(them)={them} and id(us)={self} RETURN r LIMIT 1"
        rels = self.source.cypher(q, {'them': node.id})[0]
        if not rels:
            return

        rel_model = self.definition.get('model') or StructuredRel

        return self._set_start_end_cls(rel_model.inflate(rels[0][0]), node)

    @check_source
    def all_relationships(self, node=None):
        """
        Retrieve all relationship objects between self and node.

        :param node:
        :return: [StructuredRel]
        """
        them_label = self.definition['node_class'].__label__
        rhs = 'them:' + them_label
        my_rel = _rel_helper(lhs='us', rhs=rhs, ident='r', **self.definition)
        if node:
            self._check_node(node)
            q = "MATCH " + my_rel + " WHERE id(them)={them} and id(us)={self} RETURN DISTINCT r "
            data = {'them': node.id}
        else:
            q = "MATCH " + my_rel + " WHERE id(us)={self} RETURN DISTINCT r "
            data = {}
        rels = self.source.cypher(q, data)[0]
        if not rels:
            return []

        rel_model = self.definition.get('model') or StructuredRel
        return [self._set_start_end_cls(rel_model.inflate(rel[0]), node) for rel in rels]

    def _register_place_holder(self, key):
        self._place_holder_registry[key] = self._place_holder_registry.get(key, 0) + 1
        return key + '_' + str(self._place_holder_registry[key])

    def _parse_q_filters(self, ident, q, source_class):
        target = []
        for child in q.children:
            if isinstance(child, QBase):
                q_childs = self._parse_q_filters(ident, child, source_class)
                if child.connector == Q.OR:
                    q_childs = "(" + q_childs + ")"
                target.append(q_childs)
            else:
                # for identation of relationship fields or not
                operator = ident
                kwargs = {child[0]: child[1]}

                # base filter
                filters = process_filter_args(source_class, kwargs)

                for prop, op_and_val in filters.items():
                    op, val = op_and_val
                    if op in _UNARY_OPERATORS:
                        # unary operators do not have a parameter
                        statement = '{}.{} {}'.format(operator, prop, op)
                    else:
                        place_holder = self._register_place_holder(operator + '_' + prop)
                        statement = '{}.{} {} {{{}}}'.format(operator, prop, op, place_holder)
                        self._query_params[place_holder] = val
                    target.append(statement)
        ret = ' {} '.format(q.connector).join(target)
        if q.negated:
            ret = 'NOT ({})'.format(ret)
        return ret

    @check_source
    def filter_relationships(self, node, qs=Q()):
        """
        Filter and get all relationship objects between self and node by kwargs.

        :param node:
        :param kwargs: same as `NodeSet.filter()` - Qs objects
        :return: [StructuredRel]
        """

        them_label = self.definition['node_class'].__label__
        ret = self._parse_q_filters('r', qs, self.definition['model'])
        data = self._query_params
        my_rel = _rel_helper(lhs='us', rhs='them:' + them_label, ident='r', **self.definition)
        if node:
            self._check_node(node)
            if ret:
                ret = " AND " + ret
            q = "MATCH " + my_rel + \
                " WHERE id(them)=$them AND id(us)=$self {where} RETURN DISTINCT r ".format(where=ret)
            data.update({'them': node.id})
        else:
            q = "MATCH " + my_rel + \
                " WHERE id(us)=$self AND {where} RETURN DISTINCT r ".format(where=ret)

        rels = self.source.cypher(q, data)[0]
        if not rels:
            return []

        rel_model = self.definition.get('model') or StructuredRel
        return [self._set_start_end_cls(rel_model.inflate(rel[0]), node) for rel in rels]

    def _set_start_end_cls(self, rel_instance, obj):
        if self.definition['direction'] == INCOMING:
            rel_instance._start_node_class = obj.__class__
            rel_instance._end_node_class = self.source_class
        else:
            rel_instance._start_node_class = self.source_class
            rel_instance._end_node_class = obj.__class__
        return rel_instance

    @check_source
    def reconnect(self, old_node, new_node):
        """
        Disconnect old_node and connect new_node copying over any properties on the original relationship.

        Useful for preventing cardinality violations

        :param old_node:
        :param new_node:
        :return: None
        """

        self._check_node(old_node)
        self._check_node(new_node)
        if old_node.id == new_node.id:
            return
        old_rel = _rel_helper(lhs='us', rhs='old', ident='r', **self.definition)

        # get list of properties on the existing rel
        result, meta = self.source.cypher(
            "MATCH (us), (old) WHERE id(us)={self} and id(old)={old} "
            "MATCH " + old_rel + " RETURN r", {'old': old_node.id})
        if result:
            node_properties = _get_node_properties(result[0][0])
            existing_properties = node_properties.keys()
        else:
            raise NotConnected('reconnect', self.source, old_node)

        # remove old relationship and create new one
        new_rel = _rel_helper(lhs='us', rhs='new', ident='r2', **self.definition)
        q = "MATCH (us), (old), (new) " \
            "WHERE id(us)={self} and id(old)={old} and id(new)={new} " \
            "MATCH " + old_rel
        q += " CREATE UNIQUE" + new_rel

        # copy over properties if we have
        for p in existing_properties:
            q += " SET r2.{} = r.{}".format(p, p)
        q += " WITH r DELETE r"

        self.source.cypher(q, {'old': old_node.id, 'new': new_node.id})

    @check_source
    def disconnect(self, *args, **kwargs):
        """
        Disconnect a node

        :param node:
        :return:
        """
        def run(instance, q, params, extra=None):
            rel_model = instance.definition['model']
            if hasattr(rel_model, 'before_disconnect'):
                kwargs = {
                    'start_node_id': instance.source.id,
                }
                if extra is not None and isinstance(extra, dict):
                    kwargs.update(extra)
                rel_model.before_disconnect(**kwargs)
            instance.source.cypher(q, params)

        if len(args) == 1 and isinstance(args[0], (StructuredNode, type(None))):
            node = args[0]
            if node is None:
                raise ValueError("The node argument shouldnt be none")
            # if just node provided
            rel = _rel_helper(lhs='a', rhs='b', ident='r', **self.definition)
            q = "MATCH (a), (b) WHERE id(a)={self} and id(b)={them} " \
                "MATCH " + rel + " DELETE r"

            params = {'them': node.id}
            try:
                with db.transaction:
                    run(self, q, params, {'end_node_id': node.id})
            except SystemError:
                run(self, q, params, {'end_node_id': node.id})

        elif len(args) == 1 and isinstance(args[0], Q):
            # if Q based filters provided
            node_class = self.definition['node_class']
            qb = node_class.nodes.query_builder
            try:
                match, filters = qb._parse_q_filters('b', args[0],
                                                     self.source_class, [])
            except:
                match = []
            if len(match) == 0:
                qb = self.source_class.nodes.query_builder
                match, filters = qb._parse_q_filters('b', args[0],
                                                     node_class, [])
                rel = _rel_helper(lhs='a',
                                  rhs='b:' + node_class.__label__,
                                  ident='r',
                                  **self.definition)
                q = "MATCH (a) WHERE id(a)={self} " \
                    "MATCH " + rel + " WHERE " + filters + " DELETE r"
            else:
                q = "MATCH (a) WHERE id(a)={self} " \
                    "MATCH " + " ".join(match) + " WHERE " + \
                    filters + " DELETE b_" + self.name

            params = qb._query_params
            try:
                with db.transaction:
                    run(self, q, params)
            except SystemError:
                run(self, q, params)

        elif len(args) == 1 and isinstance(args[0], NodeSet):
            # if NodeSet provided
            node_class = self.definition['node_class']
            nodeset = args[0]
            assert nodeset.source == node_class, 'class error'

            qb = nodeset.query_builder
            query, params = qb.build_query('WITH'), qb._query_params
            self._query_params.update(params)

            rel = _rel_helper(lhs='a',
                              rhs=nodeset.ident,
                              ident='r',
                              **self.definition)

            query += " MATCH (a), " + rel + " WHERE id(a)={self} DELETE r;"

            try:
                with db.transaction:
                    run(self, query, params)
            except SystemError:
                run(self, query, params)
        else:
            raise NotImplementedError('This operation not implemented yet')

    @check_source
    def disconnect_all(self):
        """
        Disconnect all nodes

        :return:
        """
        rhs = 'b:' + self.definition['node_class'].__label__
        rel = _rel_helper(lhs='a', rhs=rhs, ident='r', **self.definition)
        q = 'MATCH (a) WHERE id(a)={self} MATCH ' + rel + ' DELETE r'
        self.source.cypher(q)

    @check_source
    def _new_traversal(self):
        return Traversal(self.source, self.name, self.definition)

    # The methods below simply proxy the match engine.
    def get(self, **kwargs):
        """
        Retrieve a related node with the matching node properties.

        :param kwargs: same syntax as `NodeSet.filter()`
        :return: node
        """
        return NodeSet(self._new_traversal()).get(**kwargs)

    def get_or_none(self, **kwargs):
        """
        Retrieve a related node with the matching node properties or return None.

        :param kwargs: same syntax as `NodeSet.filter()`
        :return: node
        """
        return NodeSet(self._new_traversal()).get_or_none(**kwargs)

    @deprecated("search() is now deprecated please use filter() and exclude()")
    def search(self, **kwargs):
        """
        Retrieve related nodes matching the provided properties.

        :param kwargs: same syntax as `NodeSet.filter()`
        :return: NodeSet
        """
        return self.filter(**kwargs).all()

    def filter(self, **kwargs):
        """
        Retrieve related nodes matching the provided properties.

        :param kwargs: same syntax as `NodeSet.filter()`
        :return: NodeSet
        """
        return NodeSet(self._new_traversal()).filter(**kwargs)

    def order_by(self, *props):
        """
        Order related nodes by specified properties

        :param props:
        :return: NodeSet
        """
        return NodeSet(self._new_traversal()).order_by(*props)

    def exclude(self, **kwargs):
        """
        Exclude nodes that match the provided properties.

        :param kwargs: same syntax as `NodeSet.filter()`
        :return: NodeSet
        """
        return NodeSet(self._new_traversal()).exclude(**kwargs)

    def is_connected(self, node):
        """
        Check if a node is connected with this relationship type
        :param node:
        :return: bool
        """
        return self._new_traversal().__contains__(node)

    def single(self):
        """
        Get a single related node or none.

        :return: StructuredNode
        """
        try:
            return self[0]
        except IndexError:
            pass

    def match(self, **kwargs):
        """
        Return set of nodes who's relationship properties match supplied args

        :param kwargs: same syntax as `NodeSet.filter()`
        :return: NodeSet
        """
        return self._new_traversal().match(**kwargs)

    def all(self):
        """
        Return all related nodes.

        :return: list
        """
        return self._new_traversal().all()

    def __iter__(self):
        return self._new_traversal().__iter__()

    def __len__(self):
        return self._new_traversal().__len__()

    def __bool__(self):
        return self._new_traversal().__bool__()

    def __nonzero__(self):
        return self._new_traversal().__nonzero__()

    def __contains__(self, obj):
        return self._new_traversal().__contains__(obj)

    def __getitem__(self, key):
        return self._new_traversal().__getitem__(key)


class RelationshipDefinition(object):
    def __init__(self, relation_type, cls_name, direction, manager=RelationshipManager, model=None):
        self.module_name = sys._getframe(4).f_globals['__name__']
        if '__file__' in sys._getframe(4).f_globals:
            self.module_file = sys._getframe(4).f_globals['__file__']
        self._raw_class = cls_name
        self.manager = manager
        self.definition = {}
        self.definition['relation_type'] = relation_type
        self.definition['direction'] = direction
        self.definition['model'] = model

    def _lookup_node_class(self):
        if not isinstance(self._raw_class, basestring):
            self.definition['node_class'] = self._raw_class
        else:
            name = self._raw_class
            if name.find('.') == -1:
                module = self.module_name
            else:
                module, _, name = name.rpartition('.')

            if module not in sys.modules:
                # yet another hack to get around python semantics
                # __name__ is the namespace of the parent module for __init__.py files,
                # and the namespace of the current module for other .py files,
                # therefore there's a need to define the namespace differently for
                # these two cases in order for . in relative imports to work correctly
                # (i.e. to mean the same thing for both cases).
                # For example in the comments below, namespace == myapp, always
                if not hasattr(self, 'module_file'):
                    raise ImportError("Couldn't lookup '{}'".format(name))

                if '__init__.py' in self.module_file:
                    # e.g. myapp/__init__.py -[__name__]-> myapp
                    namespace = self.module_name
                else:
                    # e.g. myapp/models.py -[__name__]-> myapp.models
                    namespace = self.module_name.rpartition('.')[0]

                # load a module from a namespace (e.g. models from myapp)
                if module:
                    module = import_module(module, namespace).__name__
                # load the namespace itself (e.g. myapp)
                # (otherwise it would look like import . from myapp)
                else:
                    module = import_module(namespace).__name__
            self.definition['node_class'] = getattr(sys.modules[module], name)

    def build_manager(self, source, name):
        self._lookup_node_class()
        return self.manager(source, name, self.definition)


class ZeroOrMore(RelationshipManager):
    """
    A relationship of zero or more nodes (the default)
    """
    description = "zero or more relationships"


def _relate(cls_name, direction, rel_type, cardinality=None, model=None):
    if not isinstance(cls_name, (basestring, object)):
        raise ValueError('Expected class name or class got ' + repr(cls_name))

    if model and not issubclass(model, (StructuredRel,)):
        raise ValueError('model must be a StructuredRel')
    return RelationshipDefinition(rel_type, cls_name, direction, cardinality, model)


def RelationshipTo(cls_name, rel_type, cardinality=ZeroOrMore, model=None):
    return _relate(cls_name, OUTGOING, rel_type, cardinality, model)


def RelationshipFrom(cls_name, rel_type, cardinality=ZeroOrMore, model=None):
    return _relate(cls_name, INCOMING, rel_type, cardinality, model)


def Relationship(cls_name, rel_type, cardinality=ZeroOrMore, model=None):
    return _relate(cls_name, EITHER, rel_type, cardinality, model)
