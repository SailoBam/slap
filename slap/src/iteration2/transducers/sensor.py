from abc import ABC, abstractmethod
import threading
class Sensor(ABC):
    def __init__(self, transducer, identifier: str, name: str, units: str):
        self.identifier = identifier
        self.name = name
        self.units = units
        self.value = None
        self.transducer = transducer

    def getTransducer(self):
        return self.transducer        

    def getName(self):
        return self.name

    def getUnits(self):
        return self.units

    def getData(self):
        return self.value

    def setData(self, value):
        self.value = value
        
    def getIdentifier(self):
        return self.identifier

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

    
