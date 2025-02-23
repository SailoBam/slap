from .simpleModel import iterate_Heading as iterate
import msvcrt
import sys
import os
class BoatSim:

    def __init__(self, time_constant):
        # Imports constants and contains the heading variable
        self.time_constant = time_constant
        self.heading = 0

    def update(self, rudderAngle):
        # Preforms one iteration of the boats movements and ensures its a usable value
        self.heading = iterate(self.heading, rudderAngle, self.time_constant)
        self.heading = round(self.heading)
        if self.heading >= 360:
            self.heading = self.heading - 360
        elif self.heading <= 0:
            self.heading = 360 + self.heading
       
    
    def getHeading(self):
        # Returns the current heading
        return self.heading
    
if __name__ == "__main__":
    simulator = BoatSim()
    while True:
        simulator.update(1, 0.5)
        print(simulator.getHeading())