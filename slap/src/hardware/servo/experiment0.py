import RPi.GPIO as GPIO
import time

servoPIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 18 for PWM with 50Hz
p.start(2.5) # Initialization
cycle = 0
while True:
	print("Cycle is: ", cycle)
	p.ChangeDutyCycle(cycle)
	num = float(input("Enter input "))
	milli = 0.5 + float((num * 2))
	cycle = (milli / 20) * 100
