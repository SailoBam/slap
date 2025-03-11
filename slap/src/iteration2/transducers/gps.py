from control.boatSim import BoatSim
from utils.nmea.nmeaEncoder import Encoder
from control.autoPilot import AutoPilot
class Gps:
    def __init__(self):
        # Import the instance of the auto pilot


        self.encoder = Encoder()

    def setHeading(self, heading, time):
        self.auto_pilot.update(heading, time)

    def setAutoPilot(self, auto_pilot):
        self.auto_pilot = auto_pilot