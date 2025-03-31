import sys
import os
import time
from rocketModel import Rocket as RocketSim
from pidModule import PidController
from plotter import Visual
from simulator import BoatSim
from simpleModel import iterate_Heading as iterate
import math
sim = BoatSim()
visual = Visual()

# --- GAINS ---
KP = 1
KI = 0.75
KD = 0.2

target = 50
dt = 0.5

controller = PidController(KP, KI, KD)

def Main():

    pos = sim.get_Current()

    while(True):
        power = controller.pid(pos, target, dt)
        print(power)
        sim.update(power, dt)
        pos = sim.get_Current()
        visual.visual(pos)
        print(pos," ", power)

        time.sleep(0.01)


#print(sim.getPos())
Main()