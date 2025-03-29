from transducers.transducer import Transducer
from transducers.sensor import Sensor
import math
try:
    from matplotlib.cbook import ls_mapper
    import serial
    import time
    import string
    import pynmea2
    IS_RPI = True
except:
    IS_RPI = False  

class Neo6mGps(Transducer):
    def __init__(self):
        super().__init__()  # This calls the parent class's __init__
        self.heading = Sensor("Heading", "°")
        self.position = Sensor("Position", "lon, lat")
        self.sensors = [self.heading, self.position]
        self.running = False
        if IS_RPI:
            self.port = "/dev/ttyAMA0"
            self.ser = serial.Serial(self.port, baudrate=9600, timeout=0.5)

    def getLongitude(self):
        return self.lng 
    
    def getLatitude(self):
        return self.lat
    
    def run(self):
        while self.running:
            try:
                if IS_RPI:
                    newdata = self.ser.readline()
                    newdata = newdata.decode('utf-8')
                    if "GLL" in newdata:
                        newmsg=pynmea2.parse(newdata)
                        self.lat=newmsg.latitude
                        self.lng=newmsg.longitude
                        pos = f"{self.lng},{self.lat}"
                        self.position.setData(pos)
                        
                    if "HCHDG" in newdata:
                        newmsg=pynmea2.parse(newdata)
                        heading=newmsg.heading
                        self.heading.setData(heading)
                        
                else:
                    self.position.setData("50.604531, -3.408637")
                    self.heading.setData("0")
            except:
                print("Error reading GPS data")
