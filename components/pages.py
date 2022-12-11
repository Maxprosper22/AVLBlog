import cherrypy
from db import session, Chat, User, Message, Page, Post 
from components.templater import pages

class Pages:
    @cherrypy.expose
    def index(self):
        if 'username' and  'is_admin' and 'is_authenticated' not in cherrypy.session:
            cherrypy.session['username'] = 'Guest'
            cherrypy.session['is_admin'] = False
            cherrypy.session['is_authenticated'] = False
            
            print('User: ', cherrypy.session['username'], 1)
            cur_user = cherrypy.session['username']
            allpages = session.query(Page)
            
            return pages.render(cur_user=cur_user, pages=allpages)
            
        elif cherrypy.session['username'] == '':
            cherrypy.session['username'] = 'Guest'
            
            print('User: ', cherrypy.session['username'], 2)
            
        elif cherrypy.session['username'] != 'Guest':
            print(cherrypy.session['username'])
            
            allpages = session.query(Page)
            cur_user = cherrypy.session['username']
            loggedUser = session.query(User).filter(User.username == cur_user).first()
            
        
            return pages.render(cur_user=cur_user, user=loggedUser)
        