import cherrypy

class Test():
    @cherrypy.expose
    def index(self):
        return open('./templates/test.html')

    @cherrypy.expose
    def test_files(self):
        return open('./templates/file.html')