import json
import cherrypy
from cherrypy import tools
import random
from datetime import datetime

@cherrypy.tools.json_out()
def error_page_404(status, message, traceback, version):
    return {'timestamp': str(datetime.utcnow()), "Error":"404"}

class RootWS():
	__doc__ ="""
	This class / webservice will abstract all the sensor access to the 'Sense HAT' RPi
	calling it's functions will return a timestamp and a piece of data.
	start like this:
	python RPiStubWS.py
	this will startup a web server on port 9090 i.e.  http://127.0.0.1:9090/ 
	"""
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
		__doc__ = """ i.e.  http://127.0.0.1:9090/ 
		:param None
		:rtype JSON str 		
		"""
        return {'timestamp': str(datetime.utcnow()), 'index': "Hi There"}
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def temp(self):
		__doc__ = """ i.e.  http://127.0.0.1:9090/temp 
		:param None
		:rtype JSON str 		
		"""
		from sense_hat import SenseHat """ import the sense HAT library """
		sense = SenseHat() """ setup a handle for the library """
		temp = sense.get_temperature() """ get the current temp and store it in the 'temp' verable """
        return {'timestamp': str(datetime.utcnow()), 'temp': str(temp)}
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def mag(self):
		__doc__ = """ i.e.  http://127.0.0.1:9090/mag 
		:param None
		:rtype JSON str x = axis , y = axis  		
		"""
        x = str(random.randint(0,999))
        y = str(random.randint(0,999))
        return {'timestamp': str(datetime.utcnow()), 'x': str(x), 'y': str(y)}
        
def start_server():
    cherrypy.tree.mount(RootWS(), '/')
    cherrypy.config.update({'server.socket_port': 9090})
    cherrypy.engine.start()

if __name__ == '__main__':
    start_server()
