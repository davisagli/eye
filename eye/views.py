import cgi
import os
import pprint
from pyramid.response import Response
from pyramid.view import view_config
from persistent import Persistent


@view_config(path_info=r'^/$')
def index(request):
    index = open(os.path.join(os.path.dirname(__file__), 'static', 'index.html'))
    return Response(content_type='text/html', app_iter=index)
    


@view_config(renderer='json')
def repr(context, request):
    return {
        'info': cgi.escape(pprint.pformat(context.context)),
    }


@view_config(name='tree', renderer='json')
def tree(context, request):
    content_tree = _build_tree(context, 2, 1)
    if type(content_tree) == dict:
        content_tree  =  [ content_tree ] 
    
    return content_tree


def _build_tree(elem, level = 1024, remove_root = 0, id=None):
        """Levels represents how deep the tree is
        """
        if level <= 0:
            return None
        level -= 1
        
        node = {}
        children = []
        result = None
        items = elem.items()
        for k, v in items:
            result = (_build_tree(v, level, id=k))
            if result:
                children.append(result)

        if remove_root:
            return children
        else:
            node["key"] = id
            node["title"] = '%s (%s)' % (id, _get_type(elem.context))
            node["children"] = []

            if len(items):
                node["isFolder"] = True

                if not len(node["children"]):
                    node["isLazy"] = True

            node["children"] = children
            if isinstance(elem.context, Persistent):
                node['addClass'] = 'persistent'

        return node 


def _get_type(ob):
    try:
        return ob.__class__.__name__
    except AttributeError:
        return type(ob)
