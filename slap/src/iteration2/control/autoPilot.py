import control.pidModule
from services.slapStore import SlapStore, Config
from control.pidModule import PidController
from transducers.tillerActuator import TillerActuator
from threading import Thread
from utils.nmea.nmeaDecoder import Decoder
from utils.headings import angularDiff
import time
import math
import random


# If the difference between the target and actual heading is greater that
# the limit of control then fully extend the tiller
LIMIT_OF_CONTROL = 30 

class AutoPilot():

    def __init__(self):
        # Imports all the needed instances for the controller
        # Creates all needed variable for the controller
        self.thread = None
        self.data_store = SlapStore("slap.db")
        self.proportional = 0
        self.integral = 0
        self.differential = 0 
        self.pid_controller = PidController( self.proportional, self.integral, self.differential, LIMIT_OF_CONTROL)

        self.target_heading = 0
        self.decoder = Decoder()
        self.actual_heading = 0.0
        self.tiller_angle = 0.0
        self.config = None
        self.running = False
        
    def start(self):
        self.pid_controller.reset()
        self.running = True

    def stop(self):
        self.running = False

    def setHeading(self,input):
        # set Heading to the input
        self.target_heading = input
        return self.target_heading
    
    def getPilotValues(self):
        # Returns a dictionary of both heading values
        headings = {
            'target': self.target_heading,
            'tiller': self.tiller_angle
        }
        return headings
    
    def setTillerActuator(self,tiller_actuator):
        self.tiller_actuator = tiller_actuator

    def update(self, heading, time):
        # Preforms one iteration of the control
        if self.running:
            self.actual_heading = heading
            # Preforms one iteration of the PID controller
            diff = angularDiff(self.actual_heading, self.target_heading)

            if abs(diff) <= LIMIT_OF_CONTROL:
                turn_mag = self.pid_controller.pid(self.actual_heading, self.target_heading, time)
            else:
                # If we go outside the control range we must reset the PID controller
                self.pid_controller.reset()        
                if diff > 0:
                    turn_mag = 1
                elif diff < 0:
                    turn_mag = -1

            # Sets the new rudder angle to the output
            self.tiller_angle = self.tiller_actuator.setTurnMag(turn_mag)
        else:
            self.tiller_angle = 0
    


    def getHeadingError(self, target, heading):
        if target - heading <= 180:
            error = target - heading
        else:
            error = (target - heading) - 360
        return error
    
    def setPidValues(self, config: Config):
        self.config = config
        self.pid_controller.setGains(config)
    
    def getCurrentConfig(self):
        return self.config
