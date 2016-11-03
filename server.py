import cherrypy

def error_page_404(status, message, traceback, version):

    return "Oh no !! No existe u,u"

songs = {
    '1': {
        'title': 'Lumberjack Song',
        'artist': 'Canadian Guard Choir'
    },

    '2': {
        'title': 'Always Look On the Bright Side of Life',
        'artist': 'Eric Idle'
    },

    '3': {
        'title': 'Spam Spam Spam',
        'artist': 'Monty Python'
    }
}
class Songs:
    @cherrypy.tools.accept(media='text/plain')
    def GET(self, id=None):

        if id == None:
            return('Here are all the songs we have: %s' % songs)
        elif id in songs:
            song = songs[id]
            return('Song with the ID %s is called %s, and the artist is %s' % (id, song['title'], song['artist']))
        else:
            return('No song with the ID %s :-(' % id)

    exposed = True

class API:
    @cherrypy.tools.accept(media='text/plain')
    def GET(self):

        return "API MAIN PAGE"
    exposed = True

class Auth:

    def GET(self, param=""):

        try:
            return cherrypy.session['user']
        except:
            return "anonymous"

    def POST(self, user=""):

        if user=="luis":

            cherrypy.session['user'] = user
            return "Yeah!"

        else:

            return ":("

    exposed = True

class Home:

    @cherrypy.expose

    def index(self):
        return "Hola desde la app principal"

if __name__ == '__main__':

    cherrypy.tree.mount(Home(), '/', {
        '/': {
            'tools.sessions.on': True
        }
    })

    cherrypy.tree.mount(Songs(), '/api/songs',
        {'/':
            {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
        }
    )

    cherrypy.tree.mount(API(), '/api',
        {'/':
            {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
        }
    )

    cherrypy.tree.mount(Auth(), '/auth',
        {'/':
            {
            'tools.sessions.on' : True,
            'request.dispatch': cherrypy.dispatch.MethodDispatcher()},
    })
    cherrypy.config.update({'error_page.404': error_page_404})
    cherrypy.engine.start()
    cherrypy.engine.block()
