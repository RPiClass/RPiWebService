import json
import cherrypy
from cherrypy import tools
import random
from datetime import datetime

@cherrypy.tools.json_out()
def error_page_404(status, message, traceback, version):
    return {'timestamp': str(datetime.utcnow()), "Error":"404"}

class RootWS():
	@cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
	    return {'timestamp': str(datetime.utcnow()), 'index': "Hi There"}
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def temperature(self):
		from sense_hat import SenseHat 
		sense = SenseHat() 
		temp = sense.get_temperature() 
        return {'timestamp': str(datetime.utcnow()), 'temperature': str(temp)}
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def mag(self):
        x = str(random.randint(0,999))
        y = str(random.randint(0,999))
        return {'timestamp': str(datetime.utcnow()), 'x': str(x), 'y': str(y)}
        
def start_server():
    cherrypy.tree.mount(RootWS(), '/')
    cherrypy.config.update({'server.socket_port': 9090})
    cherrypy.engine.start()

if __name__ == '__main__':
    start_server()
