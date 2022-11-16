import cherrypy

# Restrict admin area
def admin_protected():
    """ RESTRICT ACCESS TO ADMIN AREA """
    # if 'username' and 'is_admin' and 'is-authenticated' not in cherrypy.session:
    #     cherrypy.session['username'] = 'Guest'
    #     cherrypy.session['is_admin'] = False
    #     cherrypy.session['is_authenticated'] = False
        
    if cherrypy.session:
        if 'username' and 'is_authenticated' and 'is_admin' not in cherrypy.session:
            # print('Authenticated: ', cherrypy.session['is_authenticated']
            print('No Session found')
            cherrypy.request.handler = cherrypy.HTTPRedirect('/login')
        elif 'username' and 'is_authenticated' and 'is_admin' in cherrypy.session:
            if not cherrypy.session['is_authenticated']:
                raise cherrypy.HTTPRedirect('/login')
            elif not cherrypy.session['is_admin']:
                raise cherrypy.HTTPRedirect('/unauthorized')
        
    elif not cherrypy.session:
        # print('User: ', cherrypy.session['username'])
        # print('Admin Priviledge: ', cherrypy.session['is_admin'])
        cherrypy.request.handler = cherrypy.HTTPRedirect('/login')
        