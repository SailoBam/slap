from geopy.distance import geodesic
from geopy.point import Point
from transducers.sensorRegister import SensorRegister
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

    def __init__(self, sensor_register: SensorRegister):
        # Imports the heading variable
        self.heading = 0.0
        self.running = False
        self.speed_over_ground = 5 #knots
        self.pos = Point(50.604531, -3.408637)
        self.sensor_register = sensor_register
        self.simThread = Thread(target=self.simulatedLoop, daemon=True)
        self.readSensorThread = Thread(target=self.readSensorLoop, daemon=True)
        # start simulation, at ~ exmouth safe water mark

        

    def setGps(self, gps):
        self.gps = gps

    def startSim(self):
        # Starts the control system on a new thread
        self.running = True
        if self.readSensorThread.is_alive():
              self.readSensorThread.join()
        self.readSensorThread.join()
        self.simThread.start()
        self.rudderAngle = 0
        
    def stopSim(self):
        # Stops the system
        print("stopSim has been run")
        self.running = False
        if self.simThread.is_alive():
              self.simThread.join()
        self.readSensorThread.start()
        self.rudderAngle = 0

    def simulatedLoop(self):
	
        while self.running:   
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

    
    def readSensorLoop(self):
        print("Trying to start real loop")
        while not self.running:
            self.currentTimeMilli = int(round(time.time() * 1000))
            print("In Real Loop")
            heading = self.sensor_register.getSensor("MagHeading").getData()
            position = self.sensor_register.getSensor("Position")
            posModule = position.getTransducer()
            longitude = posModule.getLongitude()
            latitude = posModule.getLatitude()
            self.gps.update(heading, longitude, latitude, self.currentTimeMilli)

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