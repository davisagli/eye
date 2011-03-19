import collections
import inspect

PRIMITIVES = set([int, bool, str, unicode, type(None)])


class Node(object):

    def __init__(self, context):
        self.context = context
    
    def _dict(self):
        if type(self.context) in PRIMITIVES:
            d = {}
        elif isinstance(self.context, collections.Mapping):
            d = self.context
        elif isinstance(self.context, collections.Iterable):
            d = dict((str(i), v) for i, v in enumerate(self.context))
        elif hasattr(self.context, '__Broken_state__'):
            # ZODB
            d = self.context.__Broken_state__
        else:
            d = dict(inspect.getmembers(self.context))
        
        return dict((k, Node(v)) for k,v in d.items())

    def __getitem__(self, name):
        return self._dict()[name]

    def items(self):
        return sorted(self._dict().items())
