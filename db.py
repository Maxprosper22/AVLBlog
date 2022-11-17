from sqlalchemy import create_engine, Column, String, Text, Integer, DateTime, ForeignKey, Boolean, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime

def get_date():
    return datetime.now()
    

# Remote server details

# Host: ec2-52-3-60-53.compute-1.amazonaws.com
# Database: dcalct5to7n3rm
# User: culdilrpeoznsu
# Password: 809d19ace0b87fee6fbbe03f4a2523b482f1da88c54276cb41a368b4a4e0a0a3
# URI: postgres://culdilrpeoznsu:809d19ace0b87fee6fbbe03f4a2523b482f1da88c54276cb41a368b4a4e0a0a3@ec2-52-3-60-53.compute-1.amazonaws.com:5432/dcalct5to7n3rm
    
# engine = create_engine('postgresql+psycopg2://mapro:Prosper22$$@localhost:5432/avlblogdb', echo=False)
aws_db_endpoint = 'avlblogdb.cuwtmrddsggm.us-east-1.rds.amazonaws.com'
engine = create_engine(f'postgresql+psycopg2://mapro:Prosper22$$@{aws_db_endpoint}:5432/avlblogdb', echo=False)
# engine = create_engine('postgresql+psycopg2://culdilrpeoznsu:809d19ace0b87fee6fbbe03f4a2523b482f1da88c54276cb41a368b4a4e0a0a3@ec2-52-3-60-53.compute-1.amazonaws.com:5432/dcalct5to7n3rm', echo=False)
# connect_args={'check_same_thread': False})

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

association_table = Table(
    'association_table',
    Base.metadata,
    Column('user_id', ForeignKey('users.user_id'), primary_key=True),
    Column('chat_id', ForeignKey('chats.chat_id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True)
    username = Column(String(), unique=True, nullable=False)
    password = Column(String(), nullable=False)
    email = Column(String(), nullable=False)
    admin_user = Column(Boolean, default=False)
    is_active = Column(Boolean, unique=False, default=False)
    avatar = Column(Text, nullable=True)
    date_created = Column(DateTime, default=get_date)
    posts = relationship('Post', back_populates='author')
    likes = relationship('Like', back_populates='user')
    media = relationship('Media', back_populates='user')
    authored_comments = relationship('Comment', back_populates='user')
    msgs = relationship('Message', back_populates='user')
    contact = relationship('Contact', back_populates='user')
    chats = relationship('Chat', secondary=association_table, back_populates="users")
    
    def __repr__(self):
        return f"<User {self.username}>"

class Chat(Base):
    __tablename__ = 'chats'
    
    chat_id = Column(Integer, primary_key=True)
    users = relationship('User', secondary=association_table, back_populates='chats')
    msgs = relationship('Message', back_populates='chat')
    chat_name = Column(Text)
    chat_type = Column(Text, nullable=False, default='private')
    chat_date = Column(DateTime, default=get_date())
    media = relationship('ChatMedia', back_populates='chat')
    
    def getlast(self):
        lastmsg = self.msgs[-1]
        return lastChat
        
    def repData(self):
        chatinfo = {'chat_id': self.chat_id, 'users': self.users,'msgs': self.msgs, 'chat_name': self.chat_name, 'chat_type': self.chat_type, 'chat_date': self.chat_date, 'media': self.media}
        return chatinfo
    
    def __repr__(self):
        return f'<Chat {self.chat_id}>'

class Message(Base):
    __tablename__ = 'messages'
    
    msg_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    chat_id = Column(Integer, ForeignKey('chats.chat_id'))
    user = relationship('User', back_populates='msgs')
    chat = relationship('Chat', back_populates='msgs')
    msg_txt = Column(Text, nullable=False)
    media = relationship('ChatMedia', back_populates='msg')
    date = Column(DateTime, default=get_date())
    
    def __repr__(self):
        return f"<Message {self.msg_id}>"
    
class ChatMedia(Base):
    __tablename__ = 'chatmedia'
    
    media_id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey('chats.chat_id'))
    msg_id = Column(Integer, ForeignKey('messages.msg_id'))
    # user_id = Column(Integer, ForeignKey('users.user_id'))
    path = Column(Text, nullable=False)
    date = Column(DateTime, default=get_date())
    media_type = Column(Text, nullable=False)
    
    chat = relationship('Chat', back_populates='media')
    msg = relationship('Message', back_populates='media')
    # user = relationship('User', back_populates=)
    
    def __repr__(self):
        return f'<ChatMedia {self.media_id}: {self.msg.user.username}>'
    
class Contact(Base):
    __tablename__ = 'contacts'
    contact_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    email = Column(Text, nullable=False)
    username = Column(Text, nullable=False)
    date_created = Column(DateTime, default=get_date())
    user = relationship('User', back_populates='contact')
    
    def __repr__(self):
        return f"<Contact @{self.username}: {self.user.username}>"
        
class Post(Base):
    __tablename__ = 'posts'
    
    post_id = Column(Integer, primary_key=True)
    # title = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String(50))
    date_created = Column(DateTime, default=get_date)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    author = relationship('User', back_populates='posts')
    likes = relationship('Like', back_populates='post')
    post_comments = relationship('Comment', back_populates='post')
    media_attachment = relationship('Media', back_populates='post')
    
    def __repr__(self):
        return f"<Posts {self.post_id}: {self.author.username}>"
    
class Like(Base):
    __tablename__ = 'likes'
    
    like_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.post_id'), nullable=False)
    post = relationship('Post', back_populates='likes')
    user = relationship('User', back_populates='likes')
    date = Column(DateTime, default=get_date)
    
    def __repr__(self):
        return f'<Like {self.like_id}: {self.user.username}>'
    
class Comment(Base):
    __tablename__ = 'comments'
    
    comm_id = Column(Integer, primary_key=True)
    
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.post_id'), nullable=False)
    post = relationship('Post', back_populates='post_comments')
    user = relationship('User', back_populates='authored_comments')
    comment = Column(Text, nullable=False)
    date_created = Column(DateTime, default=get_date)
    
    def __repr__(self):
        return f"<Comment {self.comm_id}: {self.user.username}>"
    
class Media(Base):
    __tablename__ = 'media'
    
    media_id = Column(Integer, primary_key=True)
    media_title = Column(String, nullable=False)
    media_path = Column(Text, nullable=False)
    media_type = Column(Text, nullable=False)
    date_created = Column(DateTime, default=get_date)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    post_id = Column(Integer, ForeignKey('posts.post_id'))
    user = relationship('User', back_populates='media')
    post = relationship('Post', back_populates='media_attachment')
    
    def __repr__(self):
        return f'Media(Title: {self.media_title}, Location: {self.media_path})'
    
Base.metadata.create_all(engine)