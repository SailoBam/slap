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

    def __init__(self, sensor_register: SensorRegister, gps):
        # Imports the heading variable
        self.gps = gps
        self.heading = 0.0 # Degrees
        self.running = False
        self.speed_over_ground = 50 #knots
        self.pos = Point(50.604531, -3.408637)
        self.sensor_register = sensor_register
        self.simThread = Thread(target=self.simulatedLoop, daemon=True)
        self.readSensorThread = Thread(target=self.readSensorLoop, daemon=True)
        

    def startSim(self):
        # Starts the control system on a new thread
        self.running = True
        if self.readSensorThread.is_alive():
            self.readSensorThread.join()
        self.simThread = Thread(target=self.simulatedLoop, daemon=True)    
        self.simThread.start()
        self.rudderAngle = 0
        
    def stopSim(self):
        # Stops the system
        self.running = False
        if self.simThread.is_alive():
            self.simThread.join()

        # Create a new thread instance for reading sensors
        self.readSensorThread = Thread(target=self.readSensorLoop, daemon=True)
        self.readSensorThread.start()
        self.rudderAngle = 0

    def simulatedLoop(self):
        while self.running: 
            # Gets current time and creates a disturbance
            self.currentTimeMilli = int(round(time.time() * 1000))
            self.nextDisturbance = self.createDisturbance()
            self.previousTime = 0
            while self.running:

                # Preforms one iteration of the boats movements and ensures its a usable value
                self.currentTimeMilli = int(round(time.time() * 1000))

                if self.previousTime != 0:
                    dt = (self.currentTimeMilli - self.previousTime) / 10**3
                else:
                    dt = 0

                # Calculate new long/lat based on distance travelled and current heading
                newPos = self.getNewPosition(self.pos, self.speed_over_ground, self.heading, dt)
                disturbance = self.disturbance()
                
                # Calculates new yaw rate based on rudder angle and disturbance
                yawRate = (1 / TIMECONSTANT) * self.rudderAngle + disturbance
                # ψ(t) = ψ(0) + δ * [t/T + (exp(-t/T) - 1)]
            
                # Calculates new heading based on yaw rate and time since last update
                newHead = (self.heading + yawRate * (dt / TIMECONSTANT + (math.exp(-dt / TIMECONSTANT) - 1))) % 360
                
                # Updates the GPS with the new heading and position
                self.gps.update(newHead, str(newPos.longitude), str(newPos.latitude), self.currentTimeMilli)
                self.heading = newHead
                self.pos = newPos
                self.previousTime = self.currentTimeMilli
    
    
    def readSensorLoop(self):
        # This is our Run Mode Loop
        # Starts reading the sensors and passing the data to the GPS
        while not self.running:
            self.currentTimeMilli = int(round(time.time() * 1000))
            heading = self.sensor_register.getSensor("MagHeading").getData()
            position = self.sensor_register.getSensor("Position")
            posModule = position.getTransducer()
            longitude = posModule.getLongitude()
            latitude = posModule.getLatitude()
            self.gps.update(heading, longitude, latitude, self.currentTimeMilli)

    def disturbance(self):
        currentTimeMilli = int(round(time.time() * 1000))

        # Checks if disturbance is active and returns the disturbance value
        # If not, creates a new disturbance
        if (currentTimeMilli < self.nextDisturbance['startTime']):
            print("time until disturbance",self.nextDisturbance['startTime'] - currentTimeMilli)
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
        # Creates a disturbance with a random magnitude and duration
        # The disturbance is a random value between -MAX_DISTURBANCE_MAGNITUDE and MAX_DISTURBANCE_MAGNITUDE
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
        # Calculate the distance travelled in km based on speed and time
        distance_km = (speed_kt * 1.852) * (time_secs / (60 * 60))  # Convert knots to km/h and compute distance
        #print(distance_km)
        return geodesic(kilometers=distance_km).destination(start_position, heading_deg)