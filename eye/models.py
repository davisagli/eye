import html
import collections.abc
import inspect
from urllib.parse import unquote
from persistent.mapping import PersistentMapping


PRIMITIVES = set([int, bool, str, type(None)])


class Node(object):

    def __init__(self, context):
        self.context = context

    def _dict(self):
        d = None

        type_ = type(self.context)
        if type_ in PRIMITIVES:
            d = {}
        elif (type_.__name__.endswith('BTree') or
              type_.__name__.endswith('TreeSet')):
            # ZODB BTrees
            d = {}
            bucket = self.context._firstbucket
            if bucket is None:
                return d
            while True:
                d[bucket.minKey()] = bucket
                bucket = bucket._next
                if bucket is None:
                    break
        elif type_.__name__.endswith('Bucket'):
            d = self.context
        elif (type_.__name__.startswith('BTrees.') and
              type_.__name__.endswith('Set')):
            d = dict(enumerate(self.context.keys()))
        elif (isinstance(self.context, collections.abc.Mapping) or
              isinstance(self.context, PersistentMapping) or
              (hasattr(self.context, 'keys') and hasattr(self.context, '__getitem__'))):
            d = self.context
        elif isinstance(self.context, collections.abc.Iterable):
            d = dict(enumerate(self.context))
        elif hasattr(self.context, '__Broken_state__'):
            # ZODB
            if isinstance(self.context.__Broken_state__, collections.abc.Mapping):
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
        d = self._dict()
        if name not in d:
            name = unquote(name)
        if name not in d and isinstance(name, bytes):
            name = name.decode('utf-8')
        return d[name]

    def items(self):
        return sorted(self._dict().items())


def _normalize(d: collections.abc.Mapping):
    d2 = {}
    for k, v in d.items():
        k = str(k).replace('/', '_')
        k = html.escape(k)
        d2[k] = Node(v)
    return d2
