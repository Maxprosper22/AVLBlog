import cherrypy
from components.templater import genSpace

class GenSpace:
    @cherrypy.expose
    def index(self, spacename):
        return genSpace.render()