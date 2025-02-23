import control.pidModule
from services.slapStore import SlapStore
from control.pidModule import PidController
from transducers.gps import Gps
from transducers.tillerActuator import TillerActuator
from threading import Thread
from utils.nmea.nmeaDecoder import Decoder

class AutoPilot():

    def __init__(self, gps: Gps, tiller_actuator: TillerActuator):
        # Imports all the needed instances for the controller
        # Creates all needed variable for the controller
        self.running = False
        self.thread = None
        self.data_store = SlapStore()
        self.pid_controller = PidController(1,0,0)
        self.gps = gps
        self.tiller_actuator = tiller_actuator
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

    def control_loop(self):
        # Preforms one iteration of the control loop
        while self.running:
            self.actual_heading = self.gps.getHeading()
            # Recieves heading and decodes the NMEA string
            self.actual_heading = self.decoder.decodeAngle(self.actual_heading)
            # Preforms one iteration of the PID controller
            angle = self.pid_controller.pid(self.actual_heading, self.target_heading, 0.01)
            # Sets the new rudder angle to the output
            self.tiller_actuator.setAngle(angle)



    def start(self):
        # Starts the control system on a new thread
        if not self.running:
            self.running = True
            self.thread = Thread(target=self.control_loop, daemon=True)
            self.thread.start()
    
    def stop(self):
        # Stops the system
        self.running = False 