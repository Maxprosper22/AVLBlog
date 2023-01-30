import cherrypy, json
from db import session, User, Chat, Message, Media, Post, ChatMedia, followers, association_table

def sortmedia(xpost):
    mediaList = []
    for x in xpost.media_attachment:
        xmedia = {'id': x.media_id, 
        'title': x.media_title,
        'path': x.media_path}
        mediaList.append(xmedia)
        
    return mediaList

def sortLike(xpost):
    likeList = []
    for x in xpost.likes:
        xlike = {
            'id': x.like_id, 
            'user_id': x.user_id,
            'page_id': x.post_id
        }
        likeList.append(xlike)
        
    return likeList

def sortComment(xpost):
    cmtList = []
    for x in xpost.post_comments:
        xCmt = {
            'id': x.comm_id, 
            'user_id': x.user_id,
            'post_id': x.post_id,
            'comment': x.comment,
            'username': x.user.username,
            'date': x.date_created.strftime("%I:%M%p %d/%m/%y")
        }
        cmtList.append(xCmt)
        
    return cmtList

class API:
    @cherrypy.expose
    def index(self):
        pass
    
    @cherrypy.expose
    @cherrypy.popargs('username')
    def home(self, username):
        if 'username' == 'Guest':
            posts = session.query(Post).all().order_by(post.date_created)
            print(posts)
            data = json.dumps(posts)
            return data
            
        else:
            user = session.query(User).filter(User.username==username).first()
            posts= []
            for post in user.followed_posts():
                dataInfo = {
                    'id': post.post_id,
                    'author': post.author.username,
                    'content': post.content,
                    'date': post.date_created.strftime("%I:%M%p %d/%m/%y"),
                    'space': post.space,
                    'page': post.page,
                    'media': sortmedia(post),
                    'comments': sortComment(post),
                    'category': post.category,
                    'likes': sortLike(post)
                }
                posts.append(dataInfo)
                # print(posts)
            return json.dumps(posts)
    
    def profile(self, username):
        pass
    
    def login(self):
        pass
    
    def follow(self, username):
        pass
    
    def messages(self, username):
        pass
    
    def create_post(self, username):
        pass
        