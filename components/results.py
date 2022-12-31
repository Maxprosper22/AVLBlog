import cherrypy
from db import session, User, Post, Space, Page 
from components.templater import result


def checkMatch(query):
    queryCaps = query.capitalize()
    nameMatch = []
    postMatch = []
    pageMatch = []
    spaceMatch = []
    
    for user in session.query(User):
        if query in user.username or queryCaps in user.username:
            nameMatch.append(user)
                
    for post in session.query(Post):
        if query in post.content or queryCaps in post.content:
            postMatch.append(post)
            
    for page in session.query(Page):
        if query in page.page_name or queryCaps in page.page_name:
            pageMatch.append(page)
            
    for space in session.query(Space):
        if query in space.space_name or queryCaps in space.space_name:
            spaceMatch.append(space)
                
    allmatches = {
        'users': nameMatch,
        'posts': postMatch,
        'pages': pageMatch,
        'spaces': spaceMatch
    }
    # print(allmatches)
    return allmatches

@cherrypy.popargs('q')
class Results:
    @cherrypy.expose
    def index(self, q):
        if 'username' and 'is_authenticated' not in cherrypy.session:
            print('First')
            cherrypy.session['username'] = 'Guest'
            curUser = cherrypy.session['username']
            allmatches = checkMatch(q)
            previews = {}
            userPreview = allmatches['users'][:3]
            postPreview = allmatches['posts'][:3]
            pagePreview = allmatches['pages'][:3]
            spacePreview = allmatches['spaces'][:3]
            
            return result.render(cur_user=curUser, matches=allmatches, query=q, user_preview=userPreview, post_preview=postPreview, page_preview=pagePreview, space_preview=spacePreview)
            
        elif cherrypy.session['username'] == '':
            print('Second')
            cherrypy.session['username'] = 'Guest'
            curUser = cherrypy.session['username']
            
            allmatches = checkMatch(q)
            previews = {}
            userPreview = allmatches['users'][:3]
            postPreview = allmatches['posts'][:3]
            pagePreview = allmatches['pages'][:3]
            spacePreview = allmatches['spaces'][:3]
            
            return result.render(cur_user=curUser, matches=allmatches, query=q, user_preview=userPreview, post_preview=postPreview, page_preview=pagePreview, space_preview=spacePreview)
            
        elif cherrypy.session['username'] == 'Guest':
            print('Third')
            curUser = cherrypy.session['username']
            
            allmatches = checkMatch(q)
            previews = {}
            userPreview = allmatches['users'][:3]
            postPreview = allmatches['posts'][:3]
            pagePreview = allmatches['pages'][:3]
            spacePreview = allmatches['spaces'][:3]
            
            return result.render(cur_user=curUser, matches=allmatches, query=q, user_preview=userPreview, post_preview=postPreview, page_preview=pagePreview, space_preview=spacePreview)
            
        elif cherrypy.session['username'] != 'Guest':
            print('Fourth')
            curUser = session.query(User).filter(User.username==cherrypy.session['username']).first()
            
            allmatches = checkMatch(q)
            previews = {}
            userPreview = allmatches['users'][:3]
            postPreview = allmatches['posts'][:3]
            pagePreview = allmatches['pages'][:3]
            spacePreview = allmatches['spaces'][:3]
            
            return result.render(cur_user=curUser, matches=allmatches, query=q, user_preview=userPreview, post_preview=postPreview, page_preview=pagePreview, space_preview=spacePreview)
        
    @cherrypy.expose
    def filter(self, *args):
        return
        
    @cherrypy.expose
    def users(self, q):
        pass
    
    @cherrypy.expose
    def pages(self, q):
        pass
    
    @cherrypy.expose
    def spaces(self, q):
        pass
    
    @cherrypy.expose
    def posts(self, q):
        pass
    