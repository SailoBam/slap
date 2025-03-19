from threading import Thread
import time
from services.slapStore import SlapStore, Trip
class Logger:

    def __init__(self):
        self.running = False

    def start(self):
        # Starts the control system on a new thread
        # 1. Create a new trip
        # slapstore.addTrip()
        if not self.running:
            self.running = True
            self.thread = Thread(target=self.loggerLoop, daemon=True)
            self.thread.start()

    def stop(self):
        # Ends the trip
        # slapStore.closeTrip()
        self.running = False


    def loggerLoop(self):
        while self.running == True:
            print("LOGGING...")
            # writes to database
            # slapStore.writeLog(tripId, logValue)
            time.sleep(5)
    
    def isRunning(self):
        return self.running
    
    def setStore(self, store: SlapStore):
        self.store = store