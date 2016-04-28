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
    def temp(self,tempResp=None,_=None):
        """ Return the current temp as an integer between 32 and 145 """
        return 'tempResp({"Temperature": ' + str(random.randint(32,100)) +'});'
        
def start_server():
    cherrypy.tree.mount(RootWS(), '/')
    cherrypy.config.update({'server.socket_port': 9090})
    cherrypy.engine.start()

if __name__ == '__main__':
    start_server()