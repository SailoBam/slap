from control.boatSim import BoatSim
from utils.nmea.nmeaEncoder import Encoder
from control.autoPilot import AutoPilot
class Gps:
    def __init__(self):
        # Import the instance of the auto pilot

        self.longitude = "0.0"
        self.latitude = "0.0"
        self.heading = 0.0
        self.encoder = Encoder()

    def update(self, heading, longitude, latitude, time):
        print("heading in gps.py is: ", heading)
        self.auto_pilot.update(heading, time)
        self.longitude = longitude
        self.latitude = latitude
        self.heading = heading

    def setAutoPilot(self, auto_pilot):
        self.auto_pilot = auto_pilot

    def getPos(self):
        pos = {'lon': self.longitude,
               'lat': self.latitude}
        return pos
        
    def getHeading(self):
        return self.heading