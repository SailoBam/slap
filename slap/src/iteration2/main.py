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

        # Produce an instance of the sensor register and add transducers to it
        self.sensor_register = SensorRegister()
        bmp280 = Bmp280Transducer()
        gps = Neo6mGps()
        magnetometer = ICM20948Magnetometer()
        self.sensor_register.add_transducer(bmp280)
        self.sensor_register.add_transducer(gps)
        self.sensor_register.add_transducer(magnetometer)
        # Start the transducers in separate threads
        self.sensor_register.run_transducers()
        
        # Init an instance of the SLAP modules
        self.tiller_actuator = TillerActuator()
        self.auto_pilot = AutoPilot()
        self.gps = Gps()
        self.boat_sim = BoatSim(self.sensor_register, self.gps)
        self.map_manager = MapManager()
        self.logger = Logger(self.gps, self.map_manager, self.sensor_register)
        self.store = SlapStore("slap.db")

        # Link classes together
        # Ensuring only one common instance of each module is used
        self.gps.setAutoPilot(self.auto_pilot)
        self.auto_pilot.setTillerActuator(self.tiller_actuator)
        self.tiller_actuator.setBoatSim(self.boat_sim)
        self.logger.setStore(self.store)


    def main(self):
        
        # Start the boat in real mode in a new thread
        self.boat_sim.stopSim()
        
        # Add each sensor to the database
        for sensor in self.sensor_register.getSensors():
            self.store.addSensor(sensor)

        # Ensure the controller stops when the application exits
        atexit.register(self.boat_sim.stopSim)

        # Create Flask web server
        webserver = WebServer(self.auto_pilot, self.logger, self.sensor_register, self.boat_sim, self.gps) 
        app = webserver.create_server(self.store)

        # Start the web server in a new thread
        app.run(debug=True, use_reloader=False, port=5000, host='0.0.0.0')


# This is where the application starts executing
if __name__ == '__main__':
    main = Main()
    main.main()
    
