
class PidController:

    def __init__(self,KP,KI,KD):
        self.kp = KP
        self.ki = KI
        self.kd = KD
        self.accumlatedError = 0
        self.lastPos = 0
        self.elapsed = 0

    def pid(self, pos, target, dt):

        # PROPORTIONAL-------
        error = target - pos
        proportional = error

        # Intergral----------
        intergal = ((error * dt) + self.accumlatedError)
        self.accumlatedError = intergal


        # Differential-------
        dpos = self.lastPos - pos
        differential = (dpos / dt)

        self.lastPos = pos

        return self.kp * proportional + self.ki * intergal + self.kd * differential