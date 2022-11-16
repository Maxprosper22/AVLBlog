import cherrypy
import json
from datetime import datetime
from components.subcomponents import b64

from db import User, Post, session, Media, Like, Comment

from components.templater import create_post, posts_list, post_details
from datetime import datetime

def get_date():
    return datetime.now()

class Posts:
    @cherrypy.expose
    def index(self):
        if 'username' and  'is_admin' and 'is_authenticated' not in cherrypy.session:
            cherrypy.session['username'] = 'Guest'
            cherrypy.session['is_admin'] = False
            cherrypy.session['is_authenticated'] = False
        print(cherrypy.session['username'])
        all_posts = session.query(Post)
        return posts_list.render(cur_user=cherrypy.session['username'],posts=all_posts)
        
    @cherrypy.expose
    @cherrypy.popargs('id')
    def post(self, id):
            
        if 'username' and  'is_admin' and 'is_authenticated' not in cherrypy.session:
            cherrypy.session['username'] = 'Guest'
            cherrypy.session['is_admin'] = False
            cherrypy.session['is_authenticated'] = False
            
        print(f'Post id: {id}')
        post_obj = session.query(Post).filter(Post.post_id==id).first()
        # print(stuff.title, stuff.post_comments)
        curUser = cherrypy.session['username']
        login_status = cherrypy.session['is_authenticated']
        return post_details.render(postObj=post_obj, cur_user=curUser, userStatus=login_status)
        
    @cherrypy.expose
    def like(self):
        likeData = json.loads(cherrypy.request.body.read())
        print(likeData)
        
        viewer = session.query(User).filter(User.username==likeData['viewer']).first()
        queryPost = session.query(Post).filter(Post.post_id==likeData['postid']).first()
        if viewer:
            for like in queryPost.likes:
                if like.user.username == likeData['viewer']:
                    session.query(Like).filter(Like.like_id==like.like_id).delete()
                    session.commit()
                    numLike = {'unlike': len(queryPost.likes)}
                    print('Took my like back!')
                    return numLike
                
                elif like.user.username != likeData['viewer']:
                    newLike = Like(post_id=likeData['postid'], user_id=viewer.user_id, post=queryPost, user=viewer)
                    session.add(newLike)
                    session.commit()
                
                    print(cherrypy.session["username"], ' likes post ', f'{likeData["postid"]}',' by ', f'{queryPost.author.username}')
                    print(len(queryPost.likes))
                    numLike = {'like': len(queryPost.likes)}
                    print('Added a like!')
                    return numLike
        else:
            return json.dumps({'err': 'User not logged in'})
    @cherrypy.expose
    def get_likes(self, postid):
        dePost = session.query(Post).filter(Post.post_id==postid).first()
        
        numLike = {'num_likes': len(dePost.likes)}
        
        return json.dumps(numLike)
        
    
    @cherrypy.expose
    def comment(self):
        pdata = json.load(cherrypy.request.body)
        print(pdata['author'])
        if pdata['author'] != 'Guest' or pdata['author'] != '':
            queryAuthor = session.query(User).filter(User.username==pdata['author']).first()
            queryPost = session.query(Post).filter(Post.post_id==pdata['postid']).first()
            newComment = Comment(user_id=queryAuthor.user_id, post_id=queryPost.post_id, user=queryAuthor, post=queryPost, comment=pdata['comment'])
            session.add(newComment)
            session.commit()
            
        else:
            return 'Error commenting'
            
        return 'Success'
        
    @cherrypy.expose        
    def create_post(self):
        if 'username' and 'is_authenticated' not in cherrypy.session:
            raise cherrypy.HTTPRedirect('/login')
            
        elif cherrypy.session['username'] == 'Guest' or cherrypy.session['is_authenticated'] == False:
            raise cherrypy.HTTPRedirect('/login')
            
        elif cherrypy.session['username'] != 'Guest' or cherrypy.session['username'] != '':
            curUser = cherrypy.session['username']
            user = session.query(User).filter(User.username==cherrypy.session['username']).first()
            return create_post.render(cur_user=curUser, user=user)
        
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def add_post(self):
        """Accepts a dictionary containing post text and image/video file (if any)"""
        if 'username' and 'is_authenticated' not in cherrypy.session:
            raise cherrypy.HTTPRedirect('/login')
        elif cherrypy.session['username'] == 'Guest' or cherrypy.session['is_authenticated'] == False:
            raise cherrypy.HTTPRedirect('/login')
            
        pdata = cherrypy.request.json
        author = session.query(User).filter(User.username==pdata['author']).first()
        
        if pdata:
            try:
                newpost = Post(content=pdata['writeup'], author=author)
                session.add(newpost)
                session.commit()
                
                lastpost = session.query(Post).filter(Post.content==newpost.content).first()
                file_list = []
                if pdata['media']:
                    for file in pdata['media']:
                        gPath = 'assets'
                        sPath = f'/media/uploads/images/{file["name"]}'
                        splitPath = sPath.split('/')
                        binPath = f'/media/uploads/bin/{file["name"]}'
                        
                        print(file['name'])
                        
                        newImg = b64.decode_file(file, gPath, sPath, binPath)
                            
                        newfile = Media(
                            media_title=file['name'],
                            media_path=newImg[1],
                            media_type=file['type'],
                            user_id=lastpost.author.user_id,
                            post_id=lastpost.post_id,
                            user=session.query(User).filter(User.user_id==lastpost.user_id).first(), post=lastpost
                        )
                        session.add(newfile)
                        session.commit()
                        file_list.append(newfile)
                    lastpost.media_attachment=[x for x in file_list]
            except Exception as e:
                print('The error is here', e)
                
        # print(cherrypy.request.json)
        # print(newpost)
        return "Post Created!"
        
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_post_media(self, postid):
        getPost = session.query(Post).filter(Post.post_id==postid).first()
        media_list = []
        for media in getPost.media_attachment:
            mediaData = {
                'title': media.media_title,
                'path': media.media_path,
                'post_id': media.post.post_id
            }
            media_list.append(json.dumps(mediaData))
        print(media_list)
            
        return media_list