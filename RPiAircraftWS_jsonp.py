import json
import cherrypy
from cherrypy import tools
import random
from datetime import datetime
from sense_hat import SenseHat
import time
import os
import glob

sense = SenseHat()

@cherrypy.tools.json_out()
def error_page_404(status, message, traceback, version):
    return {'timestamp': str(datetime.utcnow()), "Error":"404"}

class RootWS():
    @cherrypy.expose
    #@cherrypy.tools.json_out()
    def index(self):
        return {'timestamp': str(datetime.utcnow()), 'index': "Hi There"}



    
    @cherrypy.expose
    def shutdown(self):  
        cherrypy.engine.exit()
    
    
    #temperature
    @cherrypy.expose
    def temperature(self,temperatureResp=None,_=None):
        """ Return the temperature as an random integer between 32 and 145 """
        return 'temperatureResp({"temperature":   ' + str(sense.get_temperature_from_humidity()*9/5+32) +'});'

# NO JsonP editing past this point yet.

    #humidity
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def humidity(self):
        """ Return the humidity as an RANDOM integer between 0 and 100 - this value is a percentage """
        return {'timestamp': str(datetime.utcnow()), 'humidity':  str(random.randint(0,100))}

    #pressure
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def pressure(self):
        """ Return a RANDOM value of 979 - 1027 to represent millibars  """
        return {'timestamp': str(datetime.utcnow()), 'pressure':  str(sense.get_pressure())}
    
    
    #orientation
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def orientation(self):
        """ Return 3 RANDOM values representing Pitch, Roll, Yaw in Degrees  """
        return {'timestamp': str(datetime.utcnow()), 'orientation': str(sense.get_orientation_radians())}
    

    #magnetometer
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def mag(self):
        """ Return the current reading of the Magnetometer as an integer between 32 and 145 """
        return {'compass': str(sense.get_compass_raw())}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def record(self):
	from subprocess import call
	call([ "raspistill", "-n", "-o", "/home/pi/media/a%04d.jpg", "-tl", "1000", "-t", "600000", "-w", "640", "-h", "480"])
        return "Recording Started" 

    @cherrypy.expose
    def image(self):
        #imgfolder=os.path("/home/pi/media/")
        #filelist = os.listdir(imgfolder)
        #filelist = filter(lambda x: not os.path.isdir(x), filelist)
        #newest = max(filelist, key=lambda x: os.stat(x).st_mtime)
        newest=max(glob.iglob('/home/pi/media/*.jpg'), key=os.path.getctime)
        #return {'newest file': newest()}
        return newest

def start_server():
    cherrypy.tree.mount(RootWS(), '/', config=conf)
    cherrypy.config.update({'server.socket_port': 9100})
    cherrypy.engine.start()

conf = {'/media': {'tools.staticdir.on': True,
        'tools.staticdir.dir': '/home/pi/media'}}
print conf
    
if __name__ == '__main__':
    start_server()
