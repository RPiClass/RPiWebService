import json
import cherrypy
from cherrypy import tools
import random
from sense_hat import SenseHat
from datetime import datetime

sense = SenseHat()

@cherrypy.tools.json_out()
def error_page_404(status, message, traceback, version):
    return {"Error":"404"}

class RootWS():
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        return {"index": "hello world"}
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def temperature(self):
        __doc__ = """ Return the current temp  """
        return {'time': str(datetime.utcnow()), 'temperature': str(sense.get_temperature_from_humidity())}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def pressure(self):
        __doc__ = """ Return pressure in millibars"""
        return {'time': str(datetime.utcnow()), 'pressure': str(sense.get_pressure())}
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def orientation_rad(self):
        __doc__ = """ Return orientation in degrees using aircraft principles axes of pitch, roll and yaw."""
        return {'time': str(datetime.utcnow()), 'orientation_rad': str(sense.get_orientation_radians())}
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def mag(self):
        __doc__ = """ Return the current reading of the Magnetometer"""
        return {'time': str(datetime.utcnow()), 'mag': str(sense.get_compass_raw())}
        
def start_server():
    cherrypy.tree.mount(RootWS(), '/')
    cherrypy.config.update({'server.socket_port': 9090, 'server.socket_host': '0.0.0.0'})
    cherrypy.engine.start()

if __name__ == '__main__':
    start_server()
