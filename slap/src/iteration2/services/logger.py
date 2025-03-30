from threading import Thread
import time
from services.slapStore import SlapStore, Trip, Reading, Config
from datetime import datetime
from transducers.gps import Gps
from services.mapManager import MapManager
from transducers.sensorRegister import SensorRegister
class Logger:

    def __init__(self, gps: Gps, map_manager: MapManager, sensor_register: SensorRegister):
        self.running = False
        self.trip: Trip
        self.gps = gps
        self.map_manager = map_manager
        self.sensor_register = sensor_register

    def start(self, config: Config):
        # Starts the control system on a new thread
        # 1. Create a new trip
        # slapstore.addTrip()
        self.running = True
        now = datetime.now()
        date_string = now.strftime('%y %m %d %H %M %S')
        print(date_string) 
        trip = Trip(0, config.configId, now.strftime('%y %m %d %H %M %S'), 'n/a', 0.0 )   
        self.trip = self.store.createTrip(trip)
        self.running = True
        self.thread = Thread(target=self.loggerLoop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        # Ends the trip
        # slapStore.closeTrip()
        now = datetime.now()
        date_string = now.strftime('%y %m %d %H %M %S')
        self.trip.timeEnded = date_string
        self.store.endTrip(self.trip)
        # Write to map manager
        readings = self.store.getLog(self.trip)



    def loggerLoop(self):
        while self.running:
            print("LOGGING...")
            now = datetime.now()
            date_string = now.strftime('%y %m %d %H %M %S')
            pos = self.gps.getPos()
            pos_string = f"{pos['lon']}, {pos['lat']}"
            print(pos_string)
            pos_reading = Reading(self.trip.tripId, "Position", pos_string, date_string)
            self.store.writeLog(pos_reading)
            readings = self.sensor_register.getSensorReadings()
            for reading in readings:
                reading = Reading(self.trip.tripId, reading['identifier'], reading['value'], date_string)
                #print(reading)
                print("Start write")
                self.store.writeLog(reading)
                print("End write")
            # writes to database
            # slapStore.writeLog(tripId, sensorId, logValue, timeStamp)
            time.sleep(2)
    
    
    def setStore(self, store: SlapStore):
        self.store = store