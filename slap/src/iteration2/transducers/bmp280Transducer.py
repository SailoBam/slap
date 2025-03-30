try:
    from smbus2 import SMBus
    from bmp280 import BMP280
    IS_RPI = True
    print("Running on a Raspberry Pi")
except (ImportError, ModuleNotFoundError, RuntimeError):
    print("Not running on a Raspberry Pi")
    IS_RPI = False

from transducers.transducer import Transducer
import time
import threading
from transducers.sensor import Sensor

class Bmp280Transducer(Transducer):
    def __init__(self):
        super().__init__()  # This calls the parent class's __init__
        self.temperature = Sensor(self, "temperature", "Temperature", "°C")
        self.pressure = Sensor(self, "pressure", "Pressure", "hPa")
        self.sensors = [self.temperature, self.pressure]
        self.running = False
        if IS_RPI:
            self.bus = SMBus(1)
            self.bmp280 = BMP280(i2c_dev=self.bus)


    def run(self):
        """Main thread loop that continuously reads pressure"""
        while self.running:
            try:
                if IS_RPI:
                    self.pressure.setData(str(self.bmp280.get_pressure()))
                    self.temperature.setData(str(self.bmp280.get_temperature()))
                else:
                    self.pressure.setData("1013.25")  # Standard atmospheric pressure in hPa
                    self.temperature.setData("20")
                #print(f"{self.name}, Value: {self.getData()}")
                time.sleep(0.1)  # Read pressure every 100ms
            except:
                print("Error reading pressure sensor")
                time.sleep(1)  # Wait longer on error
