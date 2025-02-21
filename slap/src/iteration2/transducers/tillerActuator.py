from control.boatSim import BoatSim


class TillerActuator:

    def __init__(self, boat_sim: BoatSim):

        self.boat_sim = boat_sim


    def setAngle(self, angle):

        self.boat_sim.update(angle)