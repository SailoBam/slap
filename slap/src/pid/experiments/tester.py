import sys
import os
import time
from oneDRocket.rocketModel import Rocket as RocketSim
from pidModule import PidController
from plotter import Visual
from boatDynamics.simulator import BoatSim
from boatDynamics.simpleModel import iterate_Heading as iterate
import math
sim = BoatSim()
visual = Visual()

# --- GAINS ---
KP = 1
KI = 0.75
KD = 0

target = 0
dt = 1

controller = PidController(KP, KI, KD)

def Main():

    pos = sim.get_Current()

    while(True):
        power = controller.pid(pos, target, dt)
        #print(power)
        sim.update(power, dt)
        pos = sim.get_Current()
        visual.visual(pos)
        print(pos," ", power)

        time.sleep(0.01)


#print(sim.getPos())
Main()