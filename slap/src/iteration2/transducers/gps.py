from control.boatSim import BoatSim
from utils.nmea.nmeaEncoder import Encoder
from control.autoPilot import AutoPilot
class Gps:
    def __init__(self):
        # Import the instance of the boat simulator
        # Import the encoding functions I made

        self.encoder = Encoder()

    def setHeading(self, heading):
        self.auto_pilot.update(self.encoder.create_Angle_String(heading))

    def setAutoPilot(self, auto_pilot):
        self.auto_pilot = auto_pilot