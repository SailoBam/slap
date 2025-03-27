try:
    from smbus2 import SMBus
    from bmp280 import BMP280
    IS_RPI = True
    print("Running on a Raspberry Pi")
except (ImportError, ModuleNotFoundError, RuntimeError):
    print("Not running on a Raspberry Pi")
    IS_RPI = False

from transducers.sensor import Sensor
import time
import threading

class Pressure(Sensor):
    def __init__(self):
        super().__init__()  # This calls the parent class's __init__
        self.name = "Pressure Sensor"
        if IS_RPI:
            self.bus = SMBus(1)
            self.bmp280 = BMP280(i2c_dev=self.bus)
        else:
            self.pressure = 0
        self.running = False
        self.thread = None

    def getData(self):
        """Return the latest pressure reading"""
        return self.pressure

    def start(self):
        """Start the pressure sensor thread"""
        super().start()
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        """Stop the pressure sensor thread"""
        super().stop()
        if self.thread:
            self.thread.join()

    def run(self):
        """Main thread loop that continuously reads pressure"""
        while self.running:
            try:
                if IS_RPI:
                    self.pressure = self.bmp280.get_pressure()
                else:
                    self.pressure = 1013.25  # Standard atmospheric pressure in hPa
                #print(f"{self.name}, Value: {self.getData()}")
                time.sleep(0.1)  # Read pressure every 100ms
            except:
                print("Error reading pressure sensor")
                time.sleep(1)  # Wait longer on error
