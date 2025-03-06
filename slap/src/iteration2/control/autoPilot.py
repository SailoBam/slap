import control.pidModule
from services.slapStore import SlapStore
from control.pidModule import PidController
from transducers.tillerActuator import TillerActuator
from threading import Thread
from utils.nmea.nmeaDecoder import Decoder


# If the difference between the target and actual heading is greater that
# the limit of control then fully extend the tiller
LIMIT_OF_CONTROL = 30 

class AutoPilot():

    def __init__(self):
        # Imports all the needed instances for the controller
        # Creates all needed variable for the controller
        self.thread = None
        self.data_store = SlapStore()
        self.pid_controller = PidController( ( 1/LIMIT_OF_CONTROL ) ,0 ,0)

        self.target_heading = 0
        self.decoder = Decoder()
        self.actual_heading = 0


    def setHeading(self,input):
        # set Heading to the input
        self.target_heading = input
        return self.target_heading
    
    def getHeadings(self):
        # Returns a dictionary of both heading values
        headings = {
            'target': self.target_heading,
            'actual': self.actual_heading
        }
        return headings
    
    def setTillerActuator(self,tiller_actuator):
        self.tiller_actuator = tiller_actuator

    def update(self, heading):
        # Preforms one iteration of the control
        # Recieves heading and decodes the NMEA string
        self.actual_heading = self.decoder.decodeAngle(heading)
        # Preforms one iteration of the PID controller
        diff = self.getHeadingError(self.target_heading, self.actual_heading)

        if abs(diff) <= LIMIT_OF_CONTROL:
            turn_mag = self.pid_controller.pid(self.actual_heading, self.target_heading, 0.01)
        else:
            # If we go outside the control range we must reset the PID controller
            self.pid_controller.reset()        
            if diff > 0:
                turn_mag = 1
            elif diff < 0:
                turn_mag = -1

        # Sets the new rudder angle to the output
        self.tiller_actuator.setTurnMag(turn_mag)


    def getHeadingError(self, target, heading):
        if target - heading <= 180:
            error = target - heading
        else:
            error = (target - heading) - 360
        return error
    
    
    