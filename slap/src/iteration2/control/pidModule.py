
class PidController:

    def __init__(self,KP,KI,KD):
        # Imports the gains to be used
        self.kp = KP
        self.ki = KI
        self.kd = KD
        self.accumlatedError = 0
        self.lastPos = 0
        self.elapsed = 0

    def pid(self, pos: int, target: int, dt: float):

        # PROPORTIONAL-------
        error = target - pos
        proportional = error

        # Intergral----------
        intergal = ((error * dt) + self.accumlatedError)
        self.accumlatedError = intergal


        # Differential-------
        dpos = self.lastPos - pos
        differential = (dpos / dt)
        # Stores the previous position
        # to use in the differential equation next time it is run
        self.lastPos = pos
        # Returns the addition of all these values adjusted using the gains
        return self.kp * proportional + self.ki * intergal + self.kd * differential