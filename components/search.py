import cherrypy
from components.templater import search

class Search:
    @cherrypy.expose
    def index(self):
        if 'username' and 'is_authenticated':
            cherrypy.session['username'] = 'Guest'
        curUser = cherrypy.session['username']
        return search.render(cur_user=curUser)