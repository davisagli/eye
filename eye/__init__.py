import os
from optparse import OptionParser
import sys

from paste.httpserver import serve
from paste.fileapp import  DirectoryApp
from webob import Request

from eye.models import Node
from eye.views import as_json, as_tree

from eye import patch
patch # pyflakes

static_path = os.path.join(os.path.dirname(__file__), 'static')
static = DirectoryApp(static_path)


class Eye(object):
    """WSGI app to browse object hierarchy."""
    
    def __init__(self, root_factory):
        self.root_factory = root_factory

    def traverse(self, request):
        view = as_json
        parts = request.path.strip('/').split('/')
        if parts[-1] == '@@tree':
            parts.pop()
            view = as_tree        

        context = self.root_factory(request)
        for name in parts:
            context = context[name]
    
        return view(context)

    def __call__(self, environ, start_response):
        request = Request(environ)
    
        if request.path == '/':
            request.path_info = '/index.html'
            app = static
        elif request.path.startswith('/static/'):
            request.path_info = request.path_info[8:]
            app = static
        else:
            app = self.traverse(request)
    
        return app(environ, start_response)


def eye(root=None, zodb_uri=None, port=8080):
    """Serves a WSGI app to browse objects based on a root object or ZODB URI.
    """
    if root is not None:
        root_factory = lambda request: Node(root)
    elif zodb_uri is not None:
        if '://' not in zodb_uri:
            # treat it as a file://
            zodb_uri = 'file://' + os.path.abspath(zodb_uri)        
    
        from repoze.zodbconn.finder import PersistentApplicationFinder
        finder = PersistentApplicationFinder(zodb_uri, appmaker=lambda root: Node(root))
        root_factory = lambda request: finder(request.environ)
    else:
        raise RuntimeError("Must specify root object or ZODB URI.")
    
    app = Eye(root_factory)
    
    if 'DEBUG' in os.environ:
        from repoze.debug.pdbpm import PostMortemDebug
        app = PostMortemDebug(app)
    
    serve(app, host='127.0.0.1', port=port)


def main():
    args = sys.argv[1:]
    usage = "usage: %prog [-p port] zodb_uri"
    
    parser = OptionParser(usage=usage)
    parser.add_option("-p", "--port", dest="port",
                      help="port to serve browser on",
                      metavar="PORT", default=8080)
    (options, args) = parser.parse_args(args)
    try:
        port = int(options.port)
    except:
        parser.error('Port must be an integer.')
        sys.exit()

    if len(args) != 1:
        parser.print_help()
        sys.exit()
    zodb_uri = args[0]
    
    eye(zodb_uri=zodb_uri, port=port)


if __name__ == '__main__':
    main()
