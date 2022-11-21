from jinja2 import FileSystemLoader, Environment
from db import User, Post, session

loader = FileSystemLoader('templates')
env = Environment(loader=loader)

nav = env.get_template('nav.html')
index = env.get_template('index.html')
admin_page = env.get_template('admin.html')

posts_list = env.get_template('posts.html')
post_details = env.get_template('details.html')

logIn = env.get_template('login.html')
signUp = env.get_template('signup.html')

profile = env.get_template('profile.html')
edit = env.get_template('edit.html')

create_post = env.get_template('/admin-area/create-post.html')
managePosts = env.get_template('/admin-area/manage-posts.html')
manageUsers = env.get_template('/admin-area/manage-users.html')
req400 = env.get_template('/request400.html')
chat = env.get_template('/chat.html')
frds = env.get_template('/friends.html')
messages = env.get_template('/messages.html')
makegrp = env.get_template('/makegrp.html')
pages = env.get_template('/pages.html')

all_dir = env.get_template('/directory.html')