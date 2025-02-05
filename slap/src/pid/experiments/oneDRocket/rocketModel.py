import turtle
import time




class Rocket():
    thrust = 0
    xcor = 0
    ycor = 0
    previousYCor = 0
    g = (-9.81) #ms^-2
    maxThrust = 15
    currentVel = 0
    def capThrust(self,thrust):
        if thrust >= self.maxThrust:
            thrust = self.maxThrust
            return thrust
        elif thrust <= 0:
            thrust = 0
            return thrust
        else:
            return thrust
        

    def getPos(self):
        return self.ycor



    def update(self, power, dt):
        #power = self.capThrust(power)
        a = power + self.g
        self.currentVel = (self.previousYCor - self.ycor) / dt
        self.ycor = self.previousYCor + (self.currentVel * dt) + (0.5 * a ) * dt * dt
        self.previousYCor = self.ycor
        #print(self.ycor, " ", self.thrust)