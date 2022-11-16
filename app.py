import cherrypy
import os, time, socket
import bcrypt
from components.templater import index, admin_page, req400, managePosts, manageUsers, all_dir, logIn, signUp, chat
from db import User, Post, session, Comment
from sqlalchemy import exc
from components.subcomponents.encrypt import encrypt_pwd, verify
import smtplib
from email.message import EmailMessage

from components.post import Posts
from components.admin import Admin
from components.profile import Profile
from components.search import Search
from components.subcomponents.test import Test

from components.subcomponents.usercreation import adduser
from components.subcomponents.checkauth import check_auth

hostname = socket.gethostname()
ipadd = socket.gethostbyname(hostname)

# Register tool 'check_auth'
cherrypy.tools.auth_check = cherrypy.Tool('before_handler', check_auth)
   
# Register tool 'adduser'
cherrypy.tools.adduser = cherrypy.Tool('before_handler', adduser)


class App:
    def __init__(self):
        self.posts = Posts()
        self.admin = Admin()
        self.user = Profile()
        self.search = Search()
        self.test = Test()
        
    @cherrypy.expose
    def index(self):
        
        if 'username' and  'is_admin' and 'is_authenticated' not in cherrypy.session:
            cherrypy.session['username'] = 'Guest'
            cherrypy.session['is_admin'] = False
            cherrypy.session['is_authenticated'] = False
            
            print('User: ', cherrypy.session['username'], 1)
            
        elif cherrypy.session['username'] == '':
            cherrypy.session['username'] = 'Guest'
            
            print('User: ', cherrypy.session['username'], 2)
            
        elif cherrypy.session['username'] != 'Guest':
            print(cherrypy.session['username'])
            cur_user = cherrypy.session['username']
            loggedUser = session.query(User).filter(User.username == cur_user).first()
            
            front_page = session.query(Post)
            
            return index.render(sess=cherrypy.session, cur_user=cur_user, user=loggedUser,  frontPage=front_page)
            
        print('User: ', cherrypy.session['username'], 3)
        print('Admin: ', cherrypy.session['is_admin'])
        print('Authenticated: ', cherrypy.session['is_authenticated'])
        print('IP Address: ', ipadd)
        
        front_page = session.query(Post)
        cur_user = cherrypy.session['username']
        return index.render(sess=cherrypy.session, cur_user=cur_user, frontPage=front_page)
        
    @cherrypy.expose
    def login(self):
        if 'username' and  'is_admin' and 'is_authenticated' not in cherrypy.session:
            cherrypy.session['username'] = 'Guest'
            cherrypy.session['is_admin'] = False
            cherrypy.session['is_authenticated'] = False
            
            print('User: ', cherrypy.session['username'], 1)
            cur_user = cherrypy.session['username']
            return logIn.render(sess=cherrypy.session, cur_user=cur_user)
            
        elif cherrypy.session['username'] == '':
            cherrypy.session['username'] = 'Guest'
            print('User: ', cherrypy.session['username'], 2)
            cur_user = cherrypy.session['username']
            return logIn.render(sess=cherrypy.session, cur_user=cur_user)
            
        elif cherrypy.session['username'] != 'Guest':
            cur_user = cherrypy.session['username']
            raise cherrypy.HTTPRedirect('/')
            
        cherrypy.session['username'] = 'Guest'
        print('User: ', cherrypy.session['username'], 4)
        cur_user = cherrypy.session['username']
        return logIn.render(sess=cherrypy.session, cur_user=cur_user)
      
    @cherrypy.expose
    # @cherrypy.tools.auth_check()  
    def authenticate(self, username, password):
        req = cherrypy.request.params
        # print(cherrypy.request.__dict__)
        cherry_user = req['username']
        print(cherry_user)
        cherry_password = req['password']
        print(cherry_password)
        pwd_encode = cherry_password.encode('utf-8')
        
        # if cherry_user or cherry_password == '':
            # return req400.render()
        
        user = session.query(User).filter(User.username==cherry_user).first()
        if user:
            if bcrypt.checkpw(pwd_encode, user.password):
                            # TODO: write code...
                cherrypy.session['username'] = user.username
                cherrypy.session['is_admin'] = user.admin_user
                cherrypy.session['is_authenticated'] = True
                # Send Email On Login
                # msg = EmailMessage()
                # msg['Subject'] = 'New Login'
                # msg['From'] = 'mistymarsh44@gmail.com'
                # msg['To'] = user.email
                # msg.set_content('This is to i form you that there is a new login to your account')
                                    
                # with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    
                #     smtp.login('mistymarsh44@gmail.com', 'misty&marshy')
                    
                #     smtp.send_message(msg)
                #     print('Mail sent')
                    
                raise cherrypy.HTTPRedirect('/')
                
            if not bcrypt.checkpw(pwd_encode, userVar.password):
                return "Incorrect Password"

        else:
            return open('templates/user404.html')

    @cherrypy.expose
    def unauthorized(self):
        return open('./templates/unauthorized.html')
        
    @cherrypy.expose
    def signup(self):
        return signUp.render()
        
    # @cherrypy.tools.adduser()
    @cherrypy.expose
    def create_user(self, username, email, password):
        newuser = User(username=username, email=email, password=encrypt_pwd(password))
        print(newuser.username)
        queryUsers = session.query(User)
        for user in queryUsers:
            if user.username == newuser.username:
                return 'Username already taken'
            elif user.email == newuser.email:
                return 'This email belongs to an existing account, try another'
        
        session.add(newuser)
        session.commit()
        return 'Account Created successfully'
        
    @cherrypy.expose
    def logout(self):
        cherrypy.session['username'] = 'Guest'
        cherrypy.session['is_authenticated'] = False
        cherrypy.session['is_admin'] = False
        raise cherrypy.HTTPRedirect('/')
        
    
    @cherrypy.expose
    def comment(self, editor, postid):
        if editor == '':
            return req400.render()
        else:
            cur_user = session.query(User).filter(User.username==cherrypy.session['username']).first()
            cur_post = session.query(Post).filter(Post.post_id==postid).first()
            comment = Comment(post_id=cur_post.post_id, user_id=cur_user.user_id, comment=editor)
            session.add(comment)
            session.commit()
            raise cherrypy.HTTPRedirect(f'/posts/post/{postid}')

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.staticdir.root': os.path.abspath(os.getcwd()),
            'tools.sessions.on': True,
            # 'tools.sessions.storage_class': cherrypy.lib.sessions.FileSession,
            # 'tools.sessions.storage_path': 'site/sessions',
            # 'tools.sessions.timeout': 6
        },
        '/login': {
            # 'tools.auth_check.on': True,
            'tools.sessions.on': True,
            # 'tools.sessions.storage_class': cherrypy.lib.sessions.FileSession,
            # 'tools.sessions.storage_path': 'site/sessions'
        },
        '/static': {
			'tools.staticdir.on': True,
			'tools.staticdir.dir': 'assets'
		},
		'/static/ckeditor': {
		    'tools.staticdir.on': True,
		    'tools.staticdir.dir': 'assets'
		},
		'/posts': {
		    'tools.staticdir.root': os.path.abspath(os.getcwd())
		},
		'/admin': {
		    'tools.admin_auth_check.on': True,
		    'tools.staticdir.on': True,
		    'tools.staticdir.dir': 'assets',
		    'tools.sessions.on': True,
		  #  'tools.sessions.storage_class': cherrypy.lib.sessions.FileSession,
            # 'tools.sessions.storage_path': 'site/sessions',
		},
		'/admin/static': {
		    'tools.staticdir.on': True,
		    'tools.staticdir.dir': 'assets'
		},
		'/authenticate': {
		    'tools.auth_check.on': True,
		    'tools.sessions.on': True,
		  #  'tools.sessions.storage_class': cherrypy.lib.sessions.FileSession,
            # 'tools.sessions.storage_path': 'site/sessions',
		},
		'/posts/static': {
		    'tools.staticdir.on': True,
		    'tools.staticdir.dir': 'assets'
		},
		'/posts/post/static': {
		    'tools.staticdir.on': True,
		    'tools.staticdir.dir': 'assets'
		},
		'/posts/post/id/static': {
		    'tools.staticdir.on': True,
		    'tools.staticdir.dir': 'assets'
		},
		'/user/static': {
		    'tools.staticdir.on': True,
		    'tools.staticdir.dir': 'assets'
		},
		'/user/user/username/static': {
		    'tools.staticdir.on': True,
		    'tools.staticdir.dir': 'assets'
		}
    }
   
app = App()

# cherrypy.config.update({'environment': 'production'})
cherrypy.config.update({
    'server.ssl_module': 'pyopenssl',
    'server.ssl_certificate': './site/certificate/cert.pem',
    'server.ssl_private_key': './site/certificate/private-key.pem',
    # 'server.socket_port': 443,
    
    'server.socket_host': '0.0.0.0',
    # 'server.socket_port': int(os.environ.get('PORT', '8000')),
})
cherrypy.quickstart(App(), '/', conf)