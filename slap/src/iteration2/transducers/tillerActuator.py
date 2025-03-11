from control.boatSim import BoatSim

RUDDER_COEFFICIENT = 25

class TillerActuator():
 
    def setBoatSim(self, boat_sim: BoatSim):
        self.boat_sim = boat_sim

    def setTurnMag(self, turn_mag):
        # Preforms one iteration of the boat dynamics
        # to find the next angle on discrete time
        angle = RUDDER_COEFFICIENT * turn_mag
        self.boat_sim.setRudderAngle(angle)
        return angle