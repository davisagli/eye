import os
from optparse import OptionParser
import sys

from pyramid.config import Configurator
from paste.httpserver import serve
from eye.models import Node
from eye import patch
patch # pyflakes


def eye(root=None):
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
        return

    if root:
        def get_root(request):
            return Node(root)
    else:
        if len(args) != 1:
            parser.print_help()
            return
    
        zodb_uri = args[0]
        if '://' not in zodb_uri:
            # treat it as a file://
            zodb_uri = 'file://' + os.path.abspath(zodb_uri)        
    
        def appmaker(root):
            return Node(root)
        from repoze.zodbconn.finder import PersistentApplicationFinder
        finder = PersistentApplicationFinder(zodb_uri, appmaker)
        def get_root(request):
            return finder(request.environ)
    
    config = Configurator(root_factory = get_root)
    config.add_static_view(name='static', path='eye:static')
    import eye
    config.scan(eye)
    app = config.make_wsgi_app()
    
    if 'DEBUG' in os.environ:
        from repoze.debug.pdbpm import PostMortemDebug
        app = PostMortemDebug(app)
    
    serve(app, host='0.0.0.0', port=port)

if __name__ == '__main__':
    eye()
