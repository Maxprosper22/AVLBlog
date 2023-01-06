import cherrypy, asyncio, websockets
from components.templater import socket_test

from server import main_call

class Test():
    @cherrypy.expose
    def index(self):
        return socket_test.render()

    @cherrypy.expose
    def ws(self):
        pass
        # print(cherrypy.response.header_list)
        # asyncio.run(main_call())