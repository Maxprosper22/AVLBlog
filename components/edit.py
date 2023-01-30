import cherrypy
from components.templater import edit
from db import session, User

class Edit:
    @cherrypy.expose
    def index(self, username):
        """edit profile"""
        
        if 'username' not in cherrypy.session:
            cherrypy.session['username'] = 'Guest'
            cherrypy.session['is_authenticated'] = False
            cherrypy.session['is_admin'] = False
            viewedUser = session.query(User).filter(User.username==cherrypy.request.params['username']).first()
            curUser = cherrypy.session['username']
            
            return edit.render(cur_user=curUser, user=viewedUser)
            
    @cherrypy.expose
    def update_avatar(self, username):
        pass