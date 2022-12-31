import cherrypy
from db import session, Chat, User, Message, Page, Post 
from components.templater import page

@cherrypy.popargs('pageName')
class GenPage:
    @cherrypy.expose
    def index(self, pageName):
        if 'username' and  'is_admin' and 'is_authenticated' not in cherrypy.session:
            cherrypy.session['username'] = 'Guest'
            cherrypy.session['is_admin'] = False
            cherrypy.session['is_authenticated'] = False
            
            print('User: ', cherrypy.session['username'], 1)
            curUser = cherrypy.session['username']
            page = session.query(Page).filter(Page.page_name==pageName).first()
            
            return page.render(cur_user=curUser, page=page)
            
        elif cherrypy.session['username'] == '':
            cherrypy.session['username'] = 'Guest'
            print('User: ', cherrypy.session['username'], 2)
            curUser = cherrypy.session['username']
            page = session.query(Page).filter(Page.page_name==pageName).first()
            return page.render(cur_user=curUser, page=page)
            
        elif cherrypy.session['username'] != 'Guest':
            print(cherrypy.session['username'])
            
            page = session.query(Page)
            curUser = cherrypy.session['username']
            loggedUser = session.query(User).filter(User.username == cur_user).first()
            
        
            return page.render(cur_user=curUser, page=page)
        