#                               Project Entry Point                              # 
from services.mapManager import MapManager
from services.slapStore import SlapStore
from control.autoPilot import AutoPilot
from control.boatSim import BoatSim
from web.app import WebServer
from transducers.gps import Gps
from transducers.tillerActuator import TillerActuator
from services.logger import Logger
import threading
import time
import atexit

class Main():

    def __init__(self):
        # Init an instance of needed components
        self.tiller_actuator = TillerActuator()
        self.auto_pilot = AutoPilot()
        self.gps = Gps()
        self.boat_sim = BoatSim()
        self.map_manager = MapManager()
        self.logger = Logger(self.gps, self.map_manager)
        self.store = SlapStore()


        self.boat_sim.setGps(self.gps)
        self.gps.setAutoPilot(self.auto_pilot)
        self.auto_pilot.setTillerActuator(self.tiller_actuator)
        self.tiller_actuator.setBoatSim(self.boat_sim)
        self.logger.setStore(self.store)
        
        # import the instances into the other modules,
        # ensuring only one common instance of each module is used

    def main(self):

        # Init BoatSim
        self.boat_sim.start()

        # Ensure the controller stops when the application exits
        atexit.register(self.boat_sim.stop)

        #Create and start Flask web server
        webserver = WebServer(self.auto_pilot, self.logger) 
        app = webserver.create_server(self.store)

        app.run(debug=True, use_reloader=False)



if __name__ == '__main__':
    main = Main()
    main.main()
    
