import json
import cherrypy
from cherrypy import tools
import random

@cherrypy.tools.json_out()
def error_page_404(status, message, traceback, version):
    return {"Error":"404"}

class RootWS():
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        return {'index': "Hi There"}
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def temp(self):
        """ Return the current temp as an integer between 32 and 145 """
        return {'temp': str(random.randint(32,145))}
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def mag(self):
        """ Return the current reading of the Magnetometer as an integer between 32 and 145 """
        x = str(random.randint(0,999))
        y = str(random.randint(0,999))
        return {'x': str(x), 'y': str(y)}
        
def start_server():
    cherrypy.tree.mount(RootWS(), '/')
    cherrypy.config.update({'server.socket_port': 9090})
    cherrypy.engine.start()

if __name__ == '__main__':
    start_server()