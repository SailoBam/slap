from control.boatSim import BoatSim


class TillerActuator:
 
    def setBoatSim(self, boat_sim: BoatSim):
        self.boat_sim = boat_sim

    def setAngle(self, angle):
        # Preforms one iteration of the boat dynamics
        # to find the next angle on discrete time
        self.boat_sim.setRudderAngle(angle)