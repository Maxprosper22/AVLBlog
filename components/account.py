import cherrypy
from db import session, User, Contact

@cherrypy.popargs('username')
class Account:
    @cherrypy.expose
    def index(self, username):
        return 'Holla'