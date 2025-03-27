from geopy.distance import geodesic
from geopy.point import Point
import sys
import os
from threading import Thread
import time
import math
import random



# Used for the decay equation
TIMECONSTANT = 0.333333
MAX_DISTURBANCE_DURATION = 5000 # ms
MIN_DISTURBANCE_DURATION = 2000 # ms
MAX_DISTURBANCE_MAGNITUDE = 20 # degrees per second
class BoatSim:

    def __init__(self):
        # Imports the heading variable
        self.heading = 0.0
        self.running = False
        self.speed_over_ground = 5 #knots
        self.pos = Point(50.604531, -3.408637)
        # start simulation, at ~ exmouth safe water mark

        

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
        print("nextDisturbance", self.nextDisturbance)
        self.previousTime = 0
        while self.running == True:

            
		    

            # Preforms one iteration of the boats movements and ensures its a usable value
            self.currentTimeMilli = int(round(time.time() * 1000))

            if self.previousTime != 0:
                dt = (self.currentTimeMilli - self.previousTime) / 10**3
            else:
                dt = 0

            # Calculate new long/lat based on distance travelled and current heading
            newPos = self.getNewPosition(self.pos, self.speed_over_ground, self.heading, dt)
            disturbance = self.disturbance()
            
            print("disturbance", disturbance)

            yawRate = (1 / TIMECONSTANT) * self.rudderAngle + disturbance
            if yawRate > 0 or yawRate < 0:
                print("yawRate", yawRate)
            # ψ(t) = ψ(0) + δ * [t/T + (exp(-t/T) - 1)]
         
            newHead = (self.heading + yawRate * (dt / TIMECONSTANT + (math.exp(-dt / TIMECONSTANT) - 1))) % 360
            print("newHead", newHead)
              
            self.gps.update(newHead, str(newPos.longitude), str(newPos.latitude), self.currentTimeMilli)
            self.heading = newHead
            self.pos = newPos
            self.previousTime = self.currentTimeMilli


    def disturbance(self):
        currentTimeMilli = int(round(time.time() * 1000))

        if (currentTimeMilli < self.nextDisturbance['startTime']):
            #print("nextDisturbance['startTime']", self.nextDisturbance['startTime'])
            print("time until disturbance",self.nextDisturbance['startTime'] - currentTimeMilli)
            #print("Before")
            return 0
        elif currentTimeMilli > self.nextDisturbance['startTime'] and currentTimeMilli < self.nextDisturbance['endTime']:
            print("During")
            print("time left: " , (self.nextDisturbance['endTime'] - currentTimeMilli))
            return self.nextDisturbance['disturbance']
        else:
            print("After")
            self.nextDisturbance = self.createDisturbance()
            return 0
    
    def setRudderAngle(self,angle):
        self.previousTime = self.currentTimeMilli
        self.rudderAngle = angle

    def createDisturbance(self):
        currentTimeMilli = int(round(time.time() * 1000))
        disturbance =  random.randint(-MAX_DISTURBANCE_MAGNITUDE, MAX_DISTURBANCE_MAGNITUDE)
        startTime = currentTimeMilli + random.randint( MAX_DISTURBANCE_DURATION, 2 * MAX_DISTURBANCE_DURATION)
        endTime = startTime + random.randint(MIN_DISTURBANCE_DURATION,MAX_DISTURBANCE_DURATION)
        output = {'endTime': endTime,
                'disturbance': disturbance,
                'startTime': startTime}
        print(output)
        return output
    

    def stop(self):
        # Stops the system
        self.running = False 

    def getNewPosition(self, start_position: Point, speed_kt, heading_deg, time_secs):
        """
        Calculate the new latitude and longitude after traveling at a given speed (in knots) and heading.

        :param start_position: Where we start
        :param speed_kt: Speed in knots (nautical miles per hour)
        :param heading_deg: Compass heading in degrees (0 = North, 90 = East)
        :param time_hours: Time in hours
        :return: New (longitude, latitude) as a Point
        """

        distance_km = (speed_kt * 1.852) * (time_secs / (60 * 60))  # Convert knots to km/h and compute distance
        #print(distance_km)
        return geodesic(kilometers=distance_km).destination(start_position, heading_deg)
    



    
if __name__ == "__main__":
    simulator = BoatSim()
    while True:
        simulator.update(1, 0.5)
        print(simulator.getHeading())