from threading import Thread
import time
from services.slapStore import SlapStore, Trip, Reading
from datetime import datetime
from transducers.gps import Gps
from services.mapManager import MapManager
class Logger:

    def __init__(self, gps: Gps, map_manager: MapManager):
        self.running = False
        self.trip = None
        self.gps = gps
        self.map_manager = map_manager

    def start(self, config):
        # Starts the control system on a new thread
        # 1. Create a new trip
        # slapstore.addTrip()
        if not self.running:
            now = datetime.now()
            date_string = now.strftime('%y %m %d %H %M %S')
            print(date_string) 
            trip = Trip(None, config['configId'], now.strftime('%y %m %d %H %M %S'), None, None )   
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
        self.map_manager.uploadToMapbox(f"Slap Trip ID: {self.trip.tripId}", readings)



    def loggerLoop(self):
        while self.running == True:
            print("LOGGING...")
            now = datetime.now()
            date_string = now.strftime('%y %m %d %H %M %S')
            pos = self.gps.getPos()
            pos_string = f"{pos['lon']}, {pos['lat']}"
            print(pos_string)
            reading = Reading(self.trip.tripId, None, pos_string, date_string)
            self.store.writeLog(reading)
            # writes to database
            # slapStore.writeLog(tripId, sensorId, logValue, timeStamp)
            time.sleep(2)
    
    def isRunning(self):
        return self.running
    
    def setStore(self, store: SlapStore):
        self.store = store