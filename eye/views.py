import cgi
import json
import pprint
from webob import Response
from persistent import Persistent


def as_json(context):
    """Return an object's representation as JSON"""
    info = {
        'info': cgi.escape(pprint.pformat(context.context)),
    }
    return Response(content_type='application/json', body=json.dumps(info))


def as_tree(context):
    """Return info about an object's members as JSON"""

    tree = _build_tree(context, 2, 1)
    if type(tree) == dict:
        tree = [tree] 
    
    return Response(content_type='application/json', body=json.dumps(tree))


def _build_tree(node, level = 1024, remove_root = 0, id=None):
    if level <= 0:
        return None
    level -= 1
    
    tree = {}
    children = []
    result = None
    items = node.items()
    for k, v in items:
        result = (_build_tree(v, level, id=k))
        if result:
            children.append(result)

    if remove_root:
        return children
    else:
        tree["key"] = id
        tree["title"] = '%s (%s)' % (id, type(node.context).__name__)
        tree["children"] = []

        if len(items):
            tree["isFolder"] = True

            if not len(tree["children"]):
                tree["isLazy"] = True

        tree["children"] = children
        if isinstance(node.context, Persistent):
            tree['addClass'] = 'persistent'

    return tree
