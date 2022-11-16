import cherrypy
from db import session, Post, User
from sqlalchemy import exc
import bcrypt
import smtplib
from email.message import EmailMessage


# Add new user
def adduser():
    """ CREATE NEW USER """
    
    req = cherrypy.request
    usernm = req.params['username']
    email = req.params['email']
    password = req.params['password']
    
    query_users = session.query(User)
    
    try:
        for users in query_users:
            if usernm not in query_users:
                # Add new user to database
                encoded_pwd = password.encode('utf-8')
                pwd_encrypt = bcrypt.hashpw(encoded_pwd, bcrypt.gensalt())
                new_user = User(username=usernm, email=email, password=pwd_encrypt, is_active=True)
                session.add(new_user)
                session.commit()
                    
                # Check for newly registered user
                query_last_added = session.query(User).filter(User.username==usernm).first()
                
                # Send Email to New User
                msg = EmailMessage()
                msg['Subject'] = 'Account Creation'
                msg['From'] = 'mistymarsh44@gmail.com'
                msg['To'] = query_last_added.email
                msg.set_content('Congratulations, your account has been successfully created')
                
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

                    smtp.login('mistymarsh44@gmail.com', 'misty&marshy')

                    smtp.send_message(msg)
                    print('Mail sent')
                    
                # Log user in
                cherrypy.session['username'] = query_last_added.username
                cherrypy.session['is_authenticated'] = True
                cherrypy.session['is_admin'] = query_last_added.admin_user
                
            raise cherrypy.HTTPRedirect('/')
            
    except exc.SQLAlchemyError as e:
        print(e)
        
        session.rollback()
        