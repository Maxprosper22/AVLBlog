import cherrypy
from sqlalchemy import exc
from db import User, Post, session

# Check login details
def check_auth():
    if cherrypy.request.params['username'] and cherrypy.request.params['password'] == '':
        cherrypy.request.handler = None
        raise cherrypy.HTTPRedirect('/login')
# def check_auth():
#     """ CHECK USER LOGIN DETAILS """
    
#     req = cherrypy.request
#     cherry_user = req.params['username']
#     cherry_password = req.params['password']
#     pwd_encode = cherry_password.encode("utf-8")
    
#     print(cherrypy.request.params)
    
#     try:
#         # req.handler = None
#         # raise cherrypy.HTTPRedirect('/')
#         if cherry_user and cherry_password == '':
#             # req.handler = None
#             # return "FIELDS CANNOT BE EMPTY"
#             raise cherrypy.HTTPError(400,'FIELDS CANNOT BE EMPTY')
            
#         if cherry_user != '':
#             print("All right")
#             users = session.query(User)
#             for user in users:
#                 if cherry_user in user.username:
#                     return user
#                 elif cherry_user not in user.username:
#                     return open('templates/user404.html')
#         if cherry_password != '':
#             if bcrypt.checkpw(pwd_encode, user.password):
#                     # TODO: write code...
#                 cherrypy.session['username'] = user.username
#                 cherrypy.session['is_admin'] = user.admin_user
#                 cherrypy.session['is_authenticated'] = True
#                             # Send Email On Login
#                 # msg = EmailMessage()
#                 # msg['Subject'] = 'New Login'
#                 # msg['From'] = 'mistymarsh44@gmail.com'
#                 # msg['To'] = user.email
#                 # msg.set_content('This is to i form you that there is a new login to your account')
                                
#                 # with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                
#                 #     smtp.login('mistymarsh44@gmail.com', 'misty&marshy')
                
#                 #     smtp.send_message(msg)
#                 #     print('Mail sent')
                
#                 raise cherrypy.HTTPRedirect('/')
                
#     except exc.SQLAlchemyError as e:
#         print(e)
#         session.rollback()
#         # raise cherrypy.HTTPError(404, "User Not Found")
