import json
import cherrypy
from cherrypy import tools
import random
from sense_hat import SenseHat

sense = SenseHat()
temp = sense.get_temperature_from_humidity()
pressure = sense.get_pressure()
orientation_rad = sense.get_orientation_radians()
mag=sense.get_compass_raw()

@cherrypy.tools.json_out()
def error_page_404(status, message, traceback, version):
    return {"Error":"404"}

class RootWS():
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        return open('index.html')
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def temp(self):
        """ Return the current temp  """
        return {'temp': str(temp)}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def pressure(self):
        """ Return pressure in millibars"""
        return {'pressure': str(pressure)}
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def orientation_rad(self):
        """ Return orientation in degrees using aircraft principles axes of pitch, roll and yaw."""
        return {'orientation_rad': str(orientation_rad)}
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def mag(self):
        """ Return the current reading of the Magnetometer"""
        return {'mag': str(mag)}
        
def start_server():
    cherrypy.tree.mount(RootWS(), '/')
    cherrypy.config.update({'server.socket_port': 9090})
    cherrypy.engine.start()

if __name__ == '__main__':
    start_server()
