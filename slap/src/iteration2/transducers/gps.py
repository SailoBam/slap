from control.boatSim import BoatSim
from utils.nmea.nmeaEncoder import Encoder
class Gps:
    def __init__(self, boat_sim: BoatSim):
        self.boat_sim = boat_sim
        self.encoder = Encoder()

    def getHeading(self):
        return self.encoder.encode_Angle(self.boat_sim.getHeading())
