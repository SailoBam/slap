from abc import abstractmethod
from transducers.sensor import Sensor
import threading
class Transducer:
    def __init__(self):
        self.sensors = []
        self.running = False

    def getSensors(self) -> list[Sensor]:
        return self.sensors
    
    @abstractmethod
    def run(self):
        pass
    
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

