from abc import ABC, abstractmethod
import threading
class Sensor(ABC):
    def __init__(self, name: str, units: str):
        self.name = name
        self.units = units
        self.value = None
        
    def getName(self):
        return self.name

    def getUnits(self):
        return self.units

    def getData(self):
        return self.value

    def setData(self, value):
        self.value = value

    def start(self):
        """Start the sensor thread"""
        self.running = True
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()


    def stop(self):
        """Stop the sensor thread"""
        self.running = False
        if self.thread:
            self.thread.join()

    
