import json
import cherrypy
from cherrypy import tools
import random
import time
import serial
import string
from pynmea import nmea

@cherrypy.tools.json_out()
def error_page_404(status, message, traceback, version):
    return {"Error":"404"}  

class RootWS():
    @cherrypy.expose
    def index(self):
	return open('temp_working_sample.html')

    @cherrypy.expose
    def foo1(self):
	return open('/home/pi/Documents/altitude/index.html')
    
    @cherrypy.expose
    def release(self,releaseResp=None,_=None):
        """ Engage the sg99 servo and release the payload """
        try:
            import RPi.GPIO as GPIO
            import time    
            GPIO.setmode(GPIO.BOARD)
            PIN = 36
            GPIO.setup(PIN,GPIO.OUT)
            p = GPIO.PWM(PIN,50)
            p.start(0.0001)
            time.sleep(2)
            p.stop()
        except:
            pass
        return 'releaseResp({"releaseResp": "Dropped!"});'

    @cherrypy.expose
    def getAltitude(self,altResp=None,_=None):
	ser = serial.Serial()
	ser.port = "/dev/ttyAMA0"
	ser.baudrate = 9600
	ser.timeout = 10.0
	ser.open()
	gpgga = nmea.GPGGA()
	CURRENT_ALT = None
	while True:
	    data = ser.readline()
	    if data[0:6] == '$GPGGA':
	        gpgga.parse(data)
	        global CURRENT_ALT 
		CURRENT_ALT= gpgga.antenna_altitude
		if CURRENT_ALT:
			break

	return 'altResp({"Altitude" : "' + str(CURRENT_ALT).replace(u'\xb0',"") + '"};)'
    
    @cherrypy.expose
    def temp(self,tempResp=None,_=None):
        """ Return the current temp as an integer between 32 and 145 """
        return 'tempResp({"Temperature": ' + str(random.randint(32,100)) +'});'
        
def start_server():
    cherrypy.tree.mount(RootWS(), '/')
    cherrypy.config.update({'server.socket_port': 9090,
                            'server.socket_host': '0.0.0.0'})
    cherrypy.engine.start()

if __name__ == '__main__':
    start_server()
