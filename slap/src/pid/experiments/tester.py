import sys
import os
import time
from oneDRocket.rocketModel import Rocket
from pidModule import PidController
from plotter import Visual

sim = Rocket()
visual = Visual()

# --- GAINS ---
KP = 1
KI = 0.75
KD = 0

target = 0
dt = 1

controller = PidController(KP, KI, KD)

def Main():

    pos = sim.getPos()

    while(True):
        power = controller.pid(pos, target, dt)
        #print(power)
        sim.update(power, dt)
        pos = sim.getPos()
        visual.visual(pos)
        print(pos," ", power)

        time.sleep(0.01)


#print(sim.getPos())
Main()