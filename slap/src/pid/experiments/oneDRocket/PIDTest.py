import turtle
import time
import matplotlib.pyplot as plt
import keyboard

#GLOBALS
TICK = 0.01 #Seconds
INIT_X = 0
INIT_Y = 0
MARK_X = 15
MARK_Y = 0
MASS = 1 #kg
G = (-9.81) #ms^-2
thrust = 0
THRUST_I = 0
MAXTHRUST = 15
global velocity
velocity = 0
elapsed = 0

#------PLOT-------

x = []

#------PID-------

#---Gain---
KP = 1.0
KI = 0.02
KD = 0.005
GAIN = 0.2

#---DIFFERENTIAL---
elapsedN0 = 0
ycorN0 = 0
ycor = 0

def AddValXY(xVal):
     global x
     x.append(xVal)



def Plot(x):
     if keyboard.is_pressed("g"): 
        plt.plot(x)
        plt.show()


def Cycle():
        global elapsed
        global ycorN0
        global ycor
        error = MARK_Y - ycor
        dt = TICK
        #print(error)

        # --P--

        proportional = error * KP
        #print(proportional)
        # --I--

        et = error * elapsed
        integral = (et / dt) * KI
        #print(integral)
        # --D--
        
        dy = ycorN0 - ycor
        differential = (dy / dt) * KD
        #print(differential)
        

        
        
        # --Output--
        control = (proportional + integral + differential) * GAIN
        print(control)

        AddValXY(ycor)

        return control

class Sim():

    
    wn = turtle.Screen()

    

    def __init__(self):
        marker = turtle.Turtle()
        marker.color("red")
        marker.speed(1000)
        marker.goto(-1000,MARK_Y)
        marker.goto(1000,MARK_Y)
        marker.goto(MARK_X,MARK_Y)
        marker.penup()
        marker.goto(MARK_X,MARK_Y)
        marker.right(180)
        self.point = turtle.Turtle()
        self.point.penup()

        self.point.shape("square")
        self.point.color("black")
        self.point.right(90)


    
    def Tick(self):
        global ycorN0
        global ycor
        global elapsed
        velocity = 0
        global x

        while(True):
            elapsed = elapsed + TICK
            Plot(x)
            ycorN0 = ycor
            ycor = self.point.ycor()
            thrust = Cycle()
            if thrust >= MAXTHRUST:
                thrust = MAXTHRUST
            elif thrust <= 0:
                thrust = 0
            velocity = velocity + G + thrust
            self.point.goto(INIT_X , (self.point.ycor() + velocity))
            #print(ycor)
            #print(velocity)
            #print(thrust)
            #print(elapsed)
            time.sleep(TICK)







def Main():
    sim = Sim()
    sim.Tick()


Main()