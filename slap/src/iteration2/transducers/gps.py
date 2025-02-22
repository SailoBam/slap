from control.boatSim import BoatSim
from utils.nmea.nmeaEncoder import Encoder
class Gps:
    def __init__(self, boat_sim: BoatSim):
        # Import the instance of the boat simulator
        # Import the encoding functions I made
        self.boat_sim = boat_sim
        self.encoder = Encoder()

    def getHeading(self):
        # Returns encoded heading
        return self.encoder.encode_Angle(self.boat_sim.getHeading())
