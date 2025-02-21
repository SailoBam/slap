from .simpleModel import iterate_Heading as iterate
import msvcrt
import sys
import os
class BoatSim:

    def __init__(self, time_constant):

        self.time_constant = time_constant
        self.heading = 0

    def update(self, rudderAngle):

        self.heading = iterate(self.heading, rudderAngle, self.time_constant)
        self.heading = round(self.heading)
        if self.heading >= 360:
            self.heading = self.heading - 360
        elif self.heading <= 0:
            self.heading = 360 + self.heading
       
    
    def getHeading(self):
        return self.heading
    
if __name__ == "__main__":
    simulator = BoatSim()
    while True:
        simulator.update(1, 0.5)
        print(simulator.get_Heading())