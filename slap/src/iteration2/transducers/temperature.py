try:
    import RPi.GPIO as GPIO
    import smbus
    IS_RPI = True
    print("Running on a Raspberry Pi")
except (ImportError, ModuleNotFoundError, RuntimeError):
    print("Not running on a Raspberry Pi")
    IS_RPI = False

from transducers.sensor import Sensor
import time
import threading

class Temperature(Sensor):
    def __init__(self):
        super().__init__()  # This calls the parent class's __init__
        self.name = "Temperature Sensor"
        if IS_RPI:
            self.bus = SMBus(1)
            self.bmp280 = BMP280(i2c_dev=self.bus)
        else:
            self.temperature = 0
        self.running = False
        self.thread = None

    def get_data(self):
        """Return the latest temperature reading"""
        return self.temperature

    def start(self):
        """Start the temperature sensor thread"""
        super().start()
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        """Stop the temperature sensor thread"""
        super().stop()
        if self.thread:
            self.thread.join()

    def run(self):
        """Main thread loop that continuously reads temperature"""
        while self.running:
            try:
                if IS_RPI:
                    self.temperature = self.bmp280.get_temperature()
                else:
                    self.temperature = 20
                print(f"{self.name}, Value: {self.get_data()}")
                time.sleep(0.1)  # Read temperature every 100ms
            except:
                print("Error reading temperature sensor")
                time.sleep(1)  # Wait longer on error
