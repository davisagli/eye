import cgi
import collections
import inspect

PRIMITIVES = set([int, bool, str, unicode, type(None)])


class Node(object):

    def __init__(self, context):
        self.context = context
    
    def _dict(self):
        d = None
        
        type_ = type(self.context)
        if type_ in PRIMITIVES:
            d = {}
        elif type_.__name__.endswith('BTree'):
            # ZODB BTrees
            d = self.context
        elif isinstance(self.context, collections.Mapping):
            d = self.context
        elif isinstance(self.context, collections.Iterable):
            d = dict(enumerate(self.context))
        elif hasattr(self.context, '__Broken_state__'):
            # ZODB
            if isinstance(self.context.__Broken_state__, collections.Mapping):
                d = self.context.__Broken_state__
            else:
                d = None
        
        if d is None:
            try:
                d = dict(inspect.getmembers(self.context))
            except AttributeError:
                d = {}
        
        return _normalize(d)

    def __getitem__(self, name):
        return self._dict()[name]

    def items(self):
        return sorted(self._dict().items())


def _normalize(d):
    d2 = {}
    for k, v in d.iteritems():
        k = str(k).replace('/', '_')
        k = cgi.escape(k)
        d2[k] = Node(v)
    return d2
