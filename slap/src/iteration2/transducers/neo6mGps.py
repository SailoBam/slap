from transducers.transducer import Transducer
from transducers.sensor import Sensor
import math
try:
    import serial
    import time
    import string
    import pynmea2
    IS_RPI = True
except Exception as e:
    print(e)
    IS_RPI = False  


# This class is a transducer for the NEO-6M GPS module.
# It inherits from the Transducer class and provides methods to read GPS data.
# The class has two sensors: one for heading and one for position.
# It uses the pynmea2 library to decode NMEA 0183 protocol sentences.
class Neo6mGps(Transducer):
    def __init__(self):
        super().__init__()  # This calls the parent class's __init__
        self.heading = Sensor(self, "gpsHeading", "Heading", "°")
        self.position = Sensor(self, "gpsPosition", "Position", "lon, lat")
        self.sensors = [self.heading, self.position]
        self.running = False
        self.lng = 50
        self.lat = -3
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
                # Check if the code is running on a Raspberry Pi
                # If so, read data from the GPS module
                if IS_RPI:
                    #print("Running NEO6M")
                    newdata = self.ser.readline()
                    newdata = newdata.decode('utf-8')

                    # Returns longitude and latitude in decimal degrees
                    if "GLL" in newdata:
                        newmsg=pynmea2.parse(newdata)
                        self.lat=newmsg.latitude
                        self.lng=newmsg.longitude
                        pos = f"{self.lng},{self.lat}"
                        self.position.setData(pos)
                        
                    # Returns heading in degrees
                    if "HCHDG" in newdata:
                        newmsg=pynmea2.parse(newdata)
                        heading=newmsg.heading
                        self.heading.setData(heading)
                        
                else:
                    self.position.setData("50.604531, -3.408637")
                    self.heading.setData("0")
            except:
                print("Error reading GPS data")
