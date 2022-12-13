import cherrypy
from components.chat import Chats
from components.account import Account
from components.edit import Edit
from components.templater import profile, edit, chat, messages, frds, genPage, makegrp
from db import User, session, Message, Contact, Chat
from operator import itemgetter, attrgetter

@cherrypy.popargs('username')
class Profile:
    def __init__(self):
        self.chat = Chats()
        self.account = Account()
        self.edit = Edit()
        
    @cherrypy.expose
    def index(self, username):
        if 'username' not in cherrypy.session:
            cherrypy.session['username'] = 'Guest'
            cherrypy.session['is_authenticated'] = False
            cherrypy.session['is_admin'] = False
            viewedUser = session.query(User).filter(User.username==cherrypy.request.params['username']).first()
            curUser = cherrypy.session['username']
            
            return profile.render(cur_user=curUser, user=viewedUser)
        
        elif cherrypy.session['username'] == '':
            cherrypy.session['username'] = 'Guest'
            curUser = cherrypy.session['username']
            viewedUser = session.query(User).filter(User.username==cherrypy.request.params['username']).first()

            return profile.render(user=viewedUser, cur_user=curUser)
            
        elif cherrypy.session['username'] != 'Guest':
            curUser = cherrypy.session['username']
            loggedUser = session.query(User).filter(User.username==curUser).first()
            viewedUser = session.query(User).filter(User.username==cherrypy.request.params['username']).first()
            print('Quite close to the last one')
            return profile.render(user=viewedUser, cur_user=curUser, loggedUser=loggedUser)
                
        curUser = cherrypy.session['username']
        viewedUser = session.query(User).filter(User.username==cherrypy.request.params['username']).first()
        loggedUser = session.query(User).filter(User.username==curUser).first()
        print('There very last one')
        return profile.render(user=viewedUser, cur_user=curUser, loggedUser=loggedUser)
        
            
    @cherrypy.expose
    def messages(self, username):
        if 'username' and 'is_authenticated' not in cherrypy.session:
            cherrypy.session['username'] = 'Guest'
            cherrypy.session['is_authenticated'] = False
            
            raise cherrypy.HTTPRedirect('/login')
            
        elif cherrypy.session['username'] == '':
            cherrypy.session['username'] = 'Guest'
            
            raise cherrypy.HTTPRedirect('/login')
            
        elif cherrypy.session['username'] != 'Guest':
            curUser = cherrypy.session['username']
            loggedUser = session.query(User).filter(User.username==curUser).first()
            contactList = []
            for cnt in loggedUser.contact:
                contactList.append(cnt)
            msgs = session.query(Message)
            toSort = []
            for chat in loggedUser.chats:
                if chat.msgs:
                    chat.chat_date = chat.msgs[-1].date
                    toSort.append(chat)
                
            sortedChat = sorted(toSort, key=attrgetter('chat_date'), reverse=True)
            
            return messages.render(cur_user=curUser, loggedUser=loggedUser, chats=sortedChat, contact_list=contactList)
        
    @cherrypy.expose
    def friends(self, username):
        if 'username' and 'is_authenticated' not in cherrypy.session:
            
            
            cherrypy.session['username'] = 'Guest'
            cherrypy.session['is_authenticated'] = False
            
            raise cherrypy.HTTPRedirect('/login')
            
        chats = session.query(Chat)
        curUser = cherrypy.session['username']
        queryUser = session.query(User).filter(User.username==username).first()
        print(queryUser)
        
        return frds.render(cur_user=curUser, loggedUser=queryUser)
        
    
    @cherrypy.expose
    def create_group(self, username):
        return makegrp.render()
        
    @cherrypy.expose
    def addfrd(self, name):
        return 'Request sent!'
        
    @cherrypy.expose
    def pages(self, username):
        return genPage.render()
        