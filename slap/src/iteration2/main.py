#                               Project Entry Point                              # 

from services.slapStore import SlapStore
from control.autoPilot import AutoPilot
from control.boatSim import BoatSim
from web.app import WebServer
from transducers.gps import Gps
from transducers.tillerActuator import TillerActuator
import threading
import time
import atexit

# Used for the decay equation in boatSim
TIMECONSTANT = 0.5

class Main():

    def __init__(self):
        # Init an instance of needed components
        self.tiller_actuator = TillerActuator()
        self.auto_pilot = AutoPilot()
        self.gps = Gps()
        self.boat_sim = BoatSim(TIMECONSTANT)


        self.boat_sim.setGps(self.gps)
        self.gps.setAutoPilot(self.auto_pilot)
        self.auto_pilot.setTillerActuator(self.tiller_actuator)
        self.tiller_actuator.setBoatSim(self.boat_sim)
        
        
        # import the instances into the other modules,
        # ensuring only one common instance of each module is used

    def main(self):

        # Init BoatSim
        self.boat_sim.start()

        # Ensure the controller stops when the application exits
        atexit.register(self.boat_sim.stop)

        #Create and start Flask web server
        webserver = WebServer(self.auto_pilot)
        app = webserver.create_server()
        app.run(debug=True, use_reloader=False)



if __name__ == '__main__':

    main = Main()
    main.main()
    
