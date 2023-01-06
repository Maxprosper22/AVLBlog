import cherrypy, json
from components.templater import chat
from db import session, User, Contact, Message, Chat
from datetime import datetime

@cherrypy.popargs('xname')
class Chats:
    @cherrypy.expose
    def index(self, xname, username, chatid):
        if 'username' not in cherrypy.session:
            cherrypy.session['username'] = 'Guest'
            cherrypy.session['is_authenticated'] = False
            cherrypy.session['is_admin'] = False
            # viewedUser = session.query(User).filter(User.username==cherrypy.request.params['friend']).first()
            curUser = cherrypy.session['username']
            
            raise cherrypy.HTTPRedirect('/login')
            
        elif cherrypy.session['username'] == 'Guest' or cherrypy.session['username'] == '':
            raise cherrypy.HTTPRedirect('/login')
            
        elif cherrypy.session['username'] != 'Guest' or cherrypy.session['username'] != '' and cherrypy.session['is_authenticated'] == True:
            
            loggedUser = session.query(User).filter(User.username==cherrypy.session['username']).first()
            curUser = cherrypy.session['username']
            # chatmate = session.query(User).filter(User.username==friend).first()
            chatData = session.query(Chat).filter(Chat.chat_id==chatid).first()
            print(chatData)
            return chat.render(cur_user=curUser, loggedUser=loggedUser, chat=chatData)
            
    @cherrypy.expose
    @cherrypy.popargs('xname')
    def sendmsg(self, xname, username):
        # print(json.loads(cherrypy.request.body.read()))
        msgData = json.loads(cherrypy.request.body.read())
        curUser = cherrypy.session['username']
        loggedUser = session.query(User).filter(User.username==username).first()
        chatData = session.query(Chat).filter(Chat.chat_id==msgData['chat_id']).first()
        
        newMsg = Message(user_id=loggedUser.user_id, chat_id=chatData.chat_id, chat=chatData, user=loggedUser, msg_txt=msgData['msg_txt'])
        session.add(newMsg)
        session.commit()
    
    @cherrypy.expose
    def get_chat(self, chatid, xname, username):
        curUser = cherrypy.session['username']
        loggedUser = session.query(User).filter(User.username==username).first()
        chatData = session.query(Chat).filter(Chat.chat_id==chatid).first()
        
        lastChat = []
        lastMsg = {
            'user': chatData.msgs[-1].user.username,
            'chat_id': chatData.chat_id,
            'msg_txt': chatData.msgs[-1].msg_txt,
            'date': chatData.msgs[-1].date
        }
        lastChat.append(lastMsg)
        
        return json.dumps(lastChat)