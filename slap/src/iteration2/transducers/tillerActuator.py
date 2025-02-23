from control.boatSim import BoatSim


class TillerActuator:

    def __init__(self, boat_sim: BoatSim):
        # Import boat sim instance
        self.boat_sim = boat_sim


    def setAngle(self, angle):
        # Preforms one iteration of the boat dynamics
        # to find the next angle on discrete time
        self.boat_sim.update(angle)