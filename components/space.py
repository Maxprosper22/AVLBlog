import cherrypy
from db import session, Chat, User, Message, Page, Post, Space
from components.templater import space

@cherrypy.popargs('spaceName')
class GenSpace:
    @cherrypy.expose
    def index(self, spaceName):
        if 'username' and 'is_authenticated' not in cherrypy.session:
            cherrypy.session['username'] = 'Guest'
            cherrypy.session['is_authenticated'] = False
            
            curUser = cherrypy.session['username']
            space = session.query(Space).filter(Space.space_name).first()
            
            return space.render(cur_user=curUser, space=space)
        
        elif cherrypy.session['username'] == '':
            cherrypy.session['username'] = 'Guest'
            curUser = cherrypy.session['username']
            space = session.query(Space).filter(Space.space_name).first()
            
            return space.render(cur_user=curUser, space=space)
            
        elif cherrypy.session['username'] != 'Guest':
            print(cherrypy.session['username'])
            
            space = session.query(Space)
            curUser = cherrypy.session['username']
            loggedUser = session.query(User).filter(User.username == cur_user).first()
            
        
            return page.render(cur_user=curUser, page=page)