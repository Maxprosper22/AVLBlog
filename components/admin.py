import cherrypy

from db import User, Post, session
from components.templater import index, admin_page, req400, managePosts, manageUsers

from components.subcomponents.admin_protection import admin_protected

# Register tool 'admin_protected'
cherrypy.tools.admin_auth_check = cherrypy.Tool('before_handler', admin_protected)

class Admin:
    @cherrypy.expose
    @cherrypy.tools.admin_auth_check()
    def index(self):
        user_list = []
        post_list = []
        users = session.query(User)
        posts = session.query(Post)
        for user in users:
            user_list.append({
                'user_id': user.user_id,
                'username': user.username,
                'password': user.password,
                'email': user.email,
                'admin_user': user.admin_user,
                'is_active': user.is_active
            })
            
        for post in posts:
            post_list.append({
                'post_id': post.post_id,
                'title': post.title,
                'content': post.content,
                'category': post.category,
                'date_created': post.date_created,
                'user_id': post.user_id
            })
        print(user_list)
        print(post_list)
        return admin_page.render(users=user_list, posts=post_list)
    
    @cherrypy.expose        
    def post_creation(self):
        return create_post.render()
        
    @cherrypy.expose
    def addPost(self, title, category, content):
        print(title, '\n', category, '\n', content)
        user = session.query(User).filter(User.username==cherrypy.session['username']).first()
        newpost = Post(title=title, category=category, content=content, author=user)
        session.add(newpost)
        session.commit()
        return "Post Created!"
        
    @cherrypy.expose
    def manage_posts(self):
        all_posts = session.query(Post)
        return managePosts.render(allPosts=all_posts)
        
    
    @cherrypy.expose
    def manage_users(self):
        all_users = session.query(User)
        return manageUsers.render(allUsers=all_users)