import cherrypy, os
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import EchoWebSocket

cherrypy.config.update({'server.socket_port': 8000})
WebSocketPlugin(cherrypy.engine).subscribe()
cherrypy.tools.websocket = WebSocketTool()

class Root(object):
    @cherrypy.expose
    def index(self):
        cherrypy.response.headers['upgrade'] = 'websocket'
        return open('ws_test.html')
        # return 'some HTML with a websocket javascript connection'

    @cherrypy.expose
    def ws(self):
        # cherrypy.response.headers['upgrade'] = 'websocket'
        print(cherrypy.response)
        return open('ws_test.html')

cherrypy.quickstart(Root(), '/', config={
    '/': {
        'tools.staticdir.root': os.path.abspath(os.getcwd()),
    },
    '/static': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': 'assets'
    },
    '/ws': {
        'tools.websocket.on': True,
        'tools.websocket.handler_cls': EchoWebSocket
    }
})