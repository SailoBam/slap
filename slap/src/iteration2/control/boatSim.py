from .simpleModel import iterate_Heading as iterate
import msvcrt
import sys
import os
from threading import Thread
import time

# Used for the decay equatio
TIMECONSTANT = 0.5

class BoatSim:

    def __init__(self):
        # Imports the heading variable
        self.heading = 0
        self.running = False

    def setGps(self, gps):
        self.gps = gps

    def start(self):
        # Starts the control system on a new thread
        if not self.running:
            self.running = True
            self.thread = Thread(target=self.dynamicsLoop, daemon=True)
            self.thread.start()
            self.rudderAngle = 0
        

    def dynamicsLoop(self):
        
        previousTime = 0
        while self.running == True:
            # Preforms one iteration of the boats movements and ensures its a usable value

            currentTimeMilli = int(round(time.time() * 1000))

            if previousTime != 0:
                dt = (currentTimeMilli - previousTime) / 10**3
            else:
                dt = 0

            yawRate = (1 / TIMECONSTANT) * self.rudderAngle
            newHead = (self.heading + (yawRate * dt))% 360 # ψ(t) = ψ(0) + ∫(r) dt      
            self.gps.setHeading(newHead)
            self.heading = newHead
            previousTime = currentTimeMilli
    
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