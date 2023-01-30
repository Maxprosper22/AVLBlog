from sqlalchemy import create_engine, Column, String, Text, Integer, DateTime, ForeignKey, Boolean, Table, LargeBinary
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy_json import mutable_json_type

from datetime import datetime
import rsa

def get_date():
    return datetime.now()
    

# Remote server details

engine = create_engine('postgresql+psycopg2://postgres:C0xTiSl3ej79MyDv0J1j@containers-us-west-137.railway.app:7263/railway', echo=False)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

association_table = Table(
    'association_table',
    Base.metadata,
    Column('user_id', ForeignKey('users.user_id'), primary_key=True),
    Column('chat_id', ForeignKey('chats.chat_id'), primary_key=True)
)
followers = Table(
    'follows',
    Base.metadata,
    Column('follower_id', Integer, ForeignKey('users.user_id'), primary_key=True),
    Column('followed_id', Integer, ForeignKey('users.user_id'), primary_key=True)
)
page_follows = Table(
    'follows_table',
    Base.metadata,
    Column('user_id', ForeignKey('users.user_id'), primary_key=True),
    Column('page_id', ForeignKey('pages.page_id'), primary_key=True)
)
spaces_table = Table(
    'spaces_table',
    Base.metadata,
    Column('user_id', ForeignKey('users.user_id'), primary_key=True),
    Column('space_id', ForeignKey('spaces.space_id'), primary_key=True)
)

def createChat(ctype, chatname, visibility, **userobjs):
    newChat =Chat(chat_type=cytpe)
    newChat.users = [user for user in userobjs]
    
    if ctype == 'grp':
        newChat.chat_name = chatname
        
    if ctype == 'p2p':
        newChat.visibility = 'private'
    elif ctype == 'grp':
        newChat.visibility = visibility
        
    session.add(newChat)
    session.commit()

class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True)
    firstname = Column(String(50))
    lastname = Column(String(50))
    username = Column(String(), unique=True, nullable=False)
    password = Column(String(), nullable=False)
    email = Column(String(), nullable=False)
    bio = Column(Text)
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
    pages = relationship('Page', back_populates='user')
    spaces = relationship('Space', back_populates='user')
    followed_pages = relationship('Page', secondary=page_follows, back_populates="followers")
    followed = relationship(
        'User',
        secondary=followers,
        primaryjoin=user_id==followers.c.follower_id,
        secondaryjoin=user_id==followers.c.followed_id,
        backref='followers'
    )
    config = Column(mutable_json_type(dbtype=JSONB, nested=True))
        
    def follow(self, username):
        try:
            checkUser = session.query(User).filter(User.username==username).first()
            if checkUser != self:
                if not self.is_followed(username):
                    self.followed.append(checkUser)
                    createChat('p2p', None, 'private', [self, checkUser])
                    session.commit()
                    return f'You now follow {checkUser.username}'
                else:
                    return f'Cannot follow self'
            else:
                return f'You already follow {checkUser.username}'
        except Exception as e:
            raise e
    
    def unfollow(self, username):
        try:
            checkUser = session.query(User).filter(User.username==username).first()
        except Exception as e:
            raise e
        if checkUser != self:
            if self.is_followed(username):
                self.followed.remove(checkUser)
                session.commit()
    
    def is_followed(self, user):
        checkFollowed = session.query(User).filter(User.username==user).first()
        if checkFollowed in self.followed:
            return True
        else:
            return False
    
    def is_following(self, user):
        checkFollower = session.query(User).filter(User.username==user).first()
        if checkFollower in self.followers:
            return True
        else:
            return False
        
    def followed_posts(self):
        followedPosts = session.query(Post).join(followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id==self.user_id)
        ownPost = session.query(Post).filter(Post.user_id==self.user_id)
        return followedPosts.union(ownPost).order_by(Post.date_created.desc())
        
    def __repr__(self):
        return f"<User {self.username}>"

class Page(Base):
    __tablename__ = 'pages'
    
    page_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    post_id = Column(Integer, ForeignKey('posts.post_id'))
    page_name = Column(Text, nullable=False)
    user = relationship('User', back_populates='pages')
    posts = relationship('Post', back_populates='page')
    followers = relationship('User', secondary=page_follows, back_populates="followed_pages")
    date_created = Column(DateTime, default=get_date())
    
    def __repr__(self):
        return f"<Page: {self.page_name}, created on :{self.date_created.strft('%H:%M %a|%m|%d')}>"
        return f"<User {self.username}>"

class Space(Base):
    __tablename__ = 'spaces'
    
    space_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    post_id = Column(Integer, ForeignKey('posts.post_id'))
    space_name = Column(Text, nullable=False)
    user = relationship('User', back_populates='spaces')
    posts = relationship('Post', back_populates='space')
    members = relationship('User', secondary=spaces_table, back_populates="spaces")
    # admin = 
    date_created = Column(DateTime, default=get_date())
    
    def __repr__(self):
        return f"<Page: {self.page_name}, created on :{self.date_created.strft('%H:%M %a|%m|%d')}>"

class Chat(Base):
    __tablename__ = 'chats'
    
    chat_id = Column(Integer, primary_key=True)
    users = relationship('User', secondary=association_table, back_populates='chats')
    msgs = relationship('Message', back_populates='chat')
    chat_name = Column(Text)
    chat_type = Column(Text, nullable=False, default='p2p')
    chat_date = Column(DateTime, default=get_date())
    visibility = Column(Text, default='private')
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
    page = relationship('Page', back_populates='posts')
    space = relationship('Space', back_populates='posts')
    author = relationship('User', back_populates='posts')
    likes = relationship('Like', back_populates='post')
    post_comments = relationship('Comment', back_populates='post')
    media_attachment = relationship('Media', back_populates='post')
    
    def like_action(self, username):
        checkLike = session.query(User).filter(User.username==username).first()
        
        if is_liked(checkLike):
            newLike = Like(post_id=self.post_id, user_id=checkLike.user_id, post=self, user=checkLike)
            session.add(newLike)
            session.commit()
            
        else:
            unlike = session.query(Like).filter(Like.user==checkLike).first()
            self.likes.remove(unlike)
    
    def is_liked(self, user):
        if user in self.likes.user:
            return False
        else:
            return True
    
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
    parent_id = Column(Integer, ForeignKey('comments.comm_id'))
    replies = relationship('Comment', remote_side=[comm_id], backref='parent')
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