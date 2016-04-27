import json
import cherrypy
from cherrypy import tools
import random
from datetime import datetime
from sense_hat import SenseHat

sense = SenseHat()

@cherrypy.tools.json_out()
def error_page_404(status, message, traceback, version):
    return {'timestamp': str(datetime.utcnow()), "Error":"404"}

class RootWS():
    @cherrypy.expose
    #@cherrypy.tools.json_out()
    def index(self):
        #return {'timestamp': str(datetime.utcnow()), 'index': "Hi There"}
        #return file("index.html")
        return """<html>
<head>
        <title>CherryPy static example</title>
        <link rel="stylesheet" type="text/css" href="css/style.css" type="text/css"></link>
        <script type="application/javascript" src="js/some.js"></script>
</head>
<body>
<p>Static example</p>
<a id="shutdown"; href="./shutdown">Shutdown Server</a>
</body>
</html>"""
    
    @cherrypy.expose
    def shutdown(self):  
        cherrypy.engine.exit()
    
    
    #temperature
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def temperature(self):
        """ Return the temperature as an random integer between 32 and 145 """
        return {'timestamp': str(datetime.utcnow()), 'temperature':   str(sense.get_temperature_from_humidity())}

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
        
def start_server():
    cherrypy.tree.mount(RootWS(), '/')
    cherrypy.config.update({'server.socket_port': 9100})
    cherrypy.engine.start()

    
if __name__ == '__main__':
    start_server()
