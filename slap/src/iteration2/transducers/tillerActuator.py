from control.boatSim import BoatSim
import time
import RPi.GPIO as GPIO



RUDDER_COEFFICIENT = 25
SERVO_RANGE = 270

class TillerActuator():
    
    def __init__(self):

        servoPIN = 18
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(servoPIN, GPIO.OUT)

        self.p = GPIO.PWM(servoPIN, 50) # GPIO 18 for PWM with 50Hz
        self.p.start(0.5) # Initialization
        self.cycle = 0
 
    def setBoatSim(self, boat_sim: BoatSim):
        self.boat_sim = boat_sim

    def setTurnMag(self, turn_mag):
        print("Set Turn Mag: ", turn_mag)
        # Preforms one iteration of the boat dynamics
        # to find the next angle on discrete time
        angle = RUDDER_COEFFICIENT * turn_mag
        self.boat_sim.setRudderAngle(angle)
        self.setServo(turn_mag)
        return angle
    
    def setServo(self, turn_mag: float):
        milli = 1.5 + float(turn_mag)
        self.cycle = (milli / 20) * 100
        print("Cycle is: ", self.cycle)
        self.p.ChangeDutyCycle(self.cycle)

        
