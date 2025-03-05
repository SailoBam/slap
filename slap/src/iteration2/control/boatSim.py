from .simpleModel import iterate_Heading as iterate
import msvcrt
import sys
import os
from threading import Thread
class BoatSim:

    def __init__(self, time_constant):
        # Imports constants and contains the heading variable
        self.time_constant = time_constant
        self.heading = 0
        self.running = False

    def setGps(self, gps):
        self.gps = gps

    def start(self):
        # Starts the control system on a new thread
        if not self.running:
            self.running = True
            self.thread = Thread(target=self.controlLoop, daemon=True)
            self.thread.start()
            self.rudderAngle = 0
        

    def controlLoop(self):
        while self.running == True:
            # Preforms one iteration of the boats movements and ensures its a usable value
            self.heading = iterate(self.heading, self.rudderAngle, self.time_constant)
            self.heading = round(self.heading)
            if self.heading >= 360:
                self.heading = self.heading - 360
            elif self.heading <= 0:
                self.heading = 360 + self.heading
            self.gps.setHeading(self.heading)
    
    def setRudderAngle(self,angle):
        self.rudderAngle = angle
        
    
    def stop(self):
        # Stops the system
        self.running = False 


    
if __name__ == "__main__":
    simulator = BoatSim()
    while True:
        simulator.update(1, 0.5)
        print(simulator.getHeading())