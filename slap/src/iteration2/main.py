from services.slapStore import SlapStore
from control.autoPilot import AutoPilot
from control.boatSim import BoatSim
from web.app import WebServer
from transducers.gps import Gps
from transducers.tillerActuator import TillerActuator
import threading
import time
import atexit


TIMECONSTANT = 0.5

class Main():

    def __init__(self):
        self.boat_sim = BoatSim(TIMECONSTANT)
        self.gps = Gps(self.boat_sim)
        self.tiller_actuator = TillerActuator(self.boat_sim)
        self.auto_pilot = AutoPilot(self.gps, self.tiller_actuator)

    def main(self):

        # Init Control system
        self.auto_pilot.start()

        # Ensure the controller stops when the application exits
        atexit.register(self.auto_pilot.stop)

        #Create and start Flask web server
        webserver = WebServer(self.auto_pilot)
        app = webserver.create_server()
        app.run(debug=True, use_reloader=False)



if __name__ == '__main__':

    main = Main()
    main.main()
    
