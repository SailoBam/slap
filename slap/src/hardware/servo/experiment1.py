from rpi_hardware_pwm import HardwarePWM
import time

pwm = HardwarePWM(pwm_channel=2, hz=50, chip=2)
pwm.start(100) # full duty cycle

while True:
	print("Running")
	time.sleep(1)
	pwm.change_duty_cycle(0.5)
	time.sleep(1)
	pwm.change_duty_cycle(12.5)

pwm.stop()