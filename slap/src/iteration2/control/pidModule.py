from utils.headings import angularDiff
from services.slapStore import Config
class PidController:

    def __init__(self,KP,KI,KD, LIMIT_OF_CONTROL):
        # Imports the gains to be used
        self.kp = KP
        self.ki = KI
        self.kd = KD
        self.accumlatedError = 0
        self.lastPos = 0
        self.elapsed = 0
        self.time = 0
        self.previous_time = 0
        self.LIMIT_OF_CONTROL = LIMIT_OF_CONTROL


    def pid(self, pos: int, target: int, time: int):
        self.time = time
        intergal = 0
        differential = 0

        # PROPORTIONAL-------
        error = angularDiff(pos, target)
        proportional = error

        if self.previous_time != 0:
            dt = (self.time - self.previous_time) / 10**3
        else:
            dt = 0

        
        if dt != 0.0:
            # If this is the first run through we cannout calculate dt, so we don't find D or I

           
            # Intergral----------
            intergal = ((error * dt) + self.accumlatedError)
            self.accumlatedError = intergal


            # Differential-------
            if self.lastPos != None:

                dpos = self.lastPos - pos
                differential = (dpos / dt)
                # Stores the previous position
                # to use in the differential equation next time it is run
            else:
                differential = 0
            self.lastPos = pos

        self.previous_time = self.time
    
        # Returns the addition of all these values adjusted using the gains
        return (self.kp * proportional + self.ki * intergal + self.kd * differential) / self.LIMIT_OF_CONTROL
    
    def reset(self):
        self.accumlatedError = 0
        self.elapsed = 0
        self.lastPos = None
        self.previous_time = 0

    def setGains(self, config: Config):
        print("setting gains")
        self.kp = config.proportional
        self.ki = config.integral
        self.kd = config.differential
        self.reset()
