from abc import ABC, abstractmethod

class Sensor(ABC):
    def __init__(self):
        self.name = ""

    def get_name(self):
        return self.name

    def set_name(self, name: str):
        self.name = name

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def start(self):
        """Start the sensor thread"""
        self.running = True

    @abstractmethod
    def stop(self):
        """Stop the sensor thread"""
        self.running = False

    @abstractmethod
    def run(self):
        """Main thread loop - must be implemented by child classes"""

        pass
    
