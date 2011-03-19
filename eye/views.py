import cgi
import os
import pprint
from pyramid.response import Response
from pyramid.view import view_config
from persistent import Persistent


@view_config(path_info=r'^/$')
def index(request):
    """Render the main page"""
    index = open(os.path.join(os.path.dirname(__file__), 'static', 'index.html'))
    return Response(content_type='text/html', app_iter=index)
    


@view_config(renderer='json')
def repr(context, request):
    """Return an object's representation as JSON"""
    return {
        'info': cgi.escape(pprint.pformat(context.context)),
    }


@view_config(name='tree', renderer='json')
def tree(context, request):
    """Return info about an object's members as JSON"""

    content_tree = _build_tree(context, 2, 1)
    if type(content_tree) == dict:
        content_tree  =  [ content_tree ] 
    
    return content_tree


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
