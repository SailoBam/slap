import msvcrt
import sys
import os
from threading import Thread
import time
import math

# Used for the decay equation
TIMECONSTANT = 0.05

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
        
        self.previousTime = 0
        while self.running == True:
            # Preforms one iteration of the boats movements and ensures its a usable value

            self.currentTimeMilli = int(round(time.time() * 1000))

            if self.previousTime != 0:
                dt = (self.currentTimeMilli - self.previousTime) / 10**3
            else:
                dt = 0

            yawRate = (1 / TIMECONSTANT) * self.rudderAngle


            # ψ(t) = ψ(0) + δ * [t/T + (exp(-t/T) - 1)]

            newHead = (self.heading + yawRate * (dt / TIMECONSTANT + (math.exp(-dt / TIMECONSTANT) - 1)))
              
            self.gps.setHeading(newHead)
            self.heading = newHead

    
    def setRudderAngle(self,angle):
        self.previousTime = self.currentTimeMilli
        self.rudderAngle = angle
        
    def stop(self):
        # Stops the system
        self.running = False 


    
if __name__ == "__main__":
    simulator = BoatSim()
    while True:
        simulator.update(1, 0.5)
        print(simulator.getHeading())