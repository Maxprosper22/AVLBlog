import cherrypy

from db import User, Post, session, Comment, Page, Space

from components.results import Results
from components.templater import search

class Search:
    def __init__(self):
        self.results = Results()
        
    @cherrypy.expose
    def index(self):
        if 'username' and 'is_authenticated' not in cherrypy.session:
            cherrypy.session['username'] = 'Guest'
            curUser = cherrypy.session['username']
            
            return search.render(cur_user=curUser)
            
        elif cherrypy.session['username'] == '':
            cherrypy.session['username'] = 'Guest'
            curUser = cherrypy.session['username']
            
            return search.render(cur_user=curUser)
            
        elif cherrypy.session['username'] != 'Guest':
            curUser = session.query(User).filter(User.username==cherrypy.session['username']).first()
            
            return search.render(cur_user=curUser)