from transducers.transducer import Transducer

class SensorRegister:
    def __init__(self):
        self.transducers = []

    def add_transducer(self, transducer: Transducer):
        self.transducers.append(transducer)
        
    def get_transducers(self):
        return self.transducers
    
    def run_transducers(self):
        for transducer in self.transducers:
            transducer.start()

    def stop_transducers(self):
        for transducer in self.transducers:
            transducer.stop()

    def getSensorReadings(self):
        sensors = []
        for transducer in self.transducers:
            for sensor in transducer.getSensors():
                output = {
                    "name": sensor.getName(),
                    "value": sensor.getData(),
                    "units": sensor.getUnits()
                }
                sensors.append(output)
        return sensors
    
    


