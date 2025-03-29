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
from transducers.sensorRegister import SensorRegister
from transducers.bmp280Transducer import Bmp280Transducer
from transducers.neo6mGps import Neo6mGps
from transducers.icm20948Magnetometer import ICM20948Magnetometer
class Main():

    def __init__(self):
        # Init an instance of needed components
        self.tiller_actuator = TillerActuator()
        self.auto_pilot = AutoPilot()
        self.gps = Gps()
        self.boat_sim = BoatSim()
        self.map_manager = MapManager()
        self.logger = Logger(self.gps, self.map_manager)
        self.store = SlapStore("slap.db")


        self.boat_sim.setGps(self.gps)
        self.gps.setAutoPilot(self.auto_pilot)
        self.auto_pilot.setTillerActuator(self.tiller_actuator)
        self.tiller_actuator.setBoatSim(self.boat_sim)
        self.logger.setStore(self.store)
        # import the instances into the other modules,
        # ensuring only one common instance of each module is used
        
        # Start the transducers
        self.sensor_register = SensorRegister()
        bmp280 = Bmp280Transducer()
        gps = Neo6mGps()
        magnetometer = ICM20948Magnetometer()
        self.sensor_register.add_transducer(bmp280)
        self.sensor_register.add_transducer(gps)
        self.sensor_register.add_transducer(magnetometer)
        self.sensor_register.run_transducers()

    def main(self):
        # Ensure the controller stops when the application exits
        atexit.register(self.boat_sim.stop)

        #Create and start Flask web server
        webserver = WebServer(self.auto_pilot, self.logger, self.sensor_register, self.boat_sim, self.gps) 
        app = webserver.create_server(self.store)

        app.run(debug=True, use_reloader=False, port=5000, host='0.0.0.0')



if __name__ == '__main__':
    main = Main()
    main.main()
    
