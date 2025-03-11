import msvcrt
import sys
import os
from threading import Thread
import time
import math
import random

# Used for the decay equation
TIMECONSTANT = 0.1
MAX_DISTURBANCE_DURATION = 5000 # ms
MIN_DISTURBANCE_DURATION = 2000 # ms
MAX_DISTURBANCE_MAGNITUDE = 20 # degrees per second
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
        self.currentTimeMilli = int(round(time.time() * 1000))
        self.nextDisturbance = self.createDisturbance()
        self.previousTime = 0
        while self.running == True:
            # Preforms one iteration of the boats movements and ensures its a usable value

            self.currentTimeMilli = int(round(time.time() * 1000))

            if self.previousTime != 0:
                dt = (self.currentTimeMilli - self.previousTime) / 10**3
            else:
                dt = 0

            disturbance = self.disturbance()
            #print(disturbance)

            yawRate = (1 / TIMECONSTANT) * self.rudderAngle + disturbance


            # ψ(t) = ψ(0) + δ * [t/T + (exp(-t/T) - 1)]
         
            newHead = (self.heading + yawRate * (dt / TIMECONSTANT + (math.exp(-dt / TIMECONSTANT) - 1)))
              
            self.gps.setHeading(newHead, self.currentTimeMilli)
            self.heading = newHead


    def disturbance(self):
        currentTimeMilli = int(round(time.time() * 1000))

        if (currentTimeMilli < self.nextDisturbance['startTime']):
            #print("Before")
            return 0
        elif currentTimeMilli > self.nextDisturbance['startTime'] and currentTimeMilli < self.nextDisturbance['endTime']:
            #print("During")
            #print("time left: " , (self.nextDisturbance['endTime'] - currentTimeMilli))
            return self.nextDisturbance['disturbance']
        else:
            #print("After")
            self.nextDisturbance = self.createDisturbance()
            return 0
    
    def setRudderAngle(self,angle):
        self.previousTime = self.currentTimeMilli
        self.rudderAngle = angle

    def createDisturbance(self):
        currentTimeMilli = int(round(time.time() * 1000))
        endTime = currentTimeMilli + random.randint(MIN_DISTURBANCE_DURATION,MAX_DISTURBANCE_DURATION)
        disturbance =  random.randint(-MAX_DISTURBANCE_MAGNITUDE, MAX_DISTURBANCE_MAGNITUDE)
        startTime = currentTimeMilli + random.randint(2 * MAX_DISTURBANCE_DURATION, 5 * MAX_DISTURBANCE_DURATION)
        output = {'endTime': endTime,
                'disturbance': disturbance,
                'startTime': startTime}
        print(output)
        return output
    

    def stop(self):
        # Stops the system
        self.running = False 


    
if __name__ == "__main__":
    simulator = BoatSim()
    while True:
        simulator.update(1, 0.5)
        print(simulator.getHeading())