import cherrypy
from components.templater import search

class Search:
    @cherrypy.expose
    def index(self):
        return search.render()