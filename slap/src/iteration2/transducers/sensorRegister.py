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
                    "identifier": sensor.getIdentifier(),
                    "name": sensor.getName(),
                    "value": sensor.getData(),
                    "units": sensor.getUnits()
                }
                sensors.append(output)
        return sensors
    
    def getSensor(self, name):
        for transducer in self.transducers:
            for sensor in transducer.getSensors():
                if sensor.getName() == name:
                    return sensor
        raise Exception("No sensor found with name: " + name)

    def getSensors(self):
        sensors = []
        for transducer in self.transducers:
            for sensor in transducer.getSensors():
                sensors.append(sensor)
        return sensors
