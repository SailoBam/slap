from transducers.sensor import Sensor

class SensorRegister:
    def __init__(self):
        self.sensors = []

    def add_sensor(self, sensor: Sensor):
        self.sensors.append(sensor)

    def get_sensors(self):
        return self.sensors
    
    def run_sensors(self):
        for sensor in self.sensors:
            sensor.start()

    def stop_sensors(self):
        for sensor in self.sensors:
            sensor.stop()

    def getReadings(self):
        readings = {}
        for sensor in self.sensors:
            readings[sensor.get_name()] = sensor.getData()
            
        return readings


