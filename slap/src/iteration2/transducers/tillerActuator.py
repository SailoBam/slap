from control.boatSim import BoatSim
import time
try:
    from rpi_hardware_pwm import HardwarePWM
    IS_RPI = True
    print("Running motor from Pi")
except (ImportError, ModuleNotFoundError, RuntimeError):
    print("Not running on a Raspberry Pi")
    IS_RPI = False


# Constants for the servo motor
RUDDER_COEFFICIENT = 25
SERVO_RANGE = 270

class TillerActuator():
    
    def __init__(self):
        # Create the PWM object for the servo motor
        # This is only used when running on a Raspberry Pi
        if IS_RPI:
            # Set up the PWM channel for the servo motor
            self.p = HardwarePWM(pwm_channel=2, hz=50,chip=2)
            self.p.start(100)
            self.cycle = 0
        else:
            self.cycle = 0
 
    def setBoatSim(self, boat_sim: BoatSim):
        self.boat_sim = boat_sim

    def setTurnMag(self, turn_mag):
        # Set the turn magnitude for the boat simulation if in Sim Mode
        angle = RUDDER_COEFFICIENT * turn_mag
        self.boat_sim.setRudderAngle(angle)
        if IS_RPI:
            # Sets the servo angle based on the turn magnitude
            self.setServo(turn_mag)
        return angle
    
    def setServo(self, turn_mag: float):
        # The PWM signals function between a range of 0.5ms to 2.5ms
        # The centre point therefore being 1.5ms
        milli = 1.5 + float(turn_mag)
        self.cycle = (milli / 20) * 100
        print("Cycle is: ", self.cycle)
        self.p.change_duty_cycle(self.cycle)

        
