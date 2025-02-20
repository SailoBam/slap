import sys
import os
import time
from boatDynamics.gpsSim import BoatSim as GpsSim
from nmea.nmeaDecoder import Decoder
from pid.pidModule import PidController
from visuals.liveCompass import Visual
from database.slapStore import Boat
from database.slapStore import SlapStore
from database.slapStore import Reading
from datetime import datetime
from webapp.app import updateTarget
from webapp.app import run_flask
import msvcrt
import threading
from flask import Flask, render_template, request, jsonify
import queue



class MainLoop:
    def main(self):
        print("Running Main")
        heading = 83
        timeConstant = 0.5
        dt = 0.01
        power = 0 
        target = 85
        gps = GpsSim()
        decoder = Decoder()
        visual = Visual(target)
        store = SlapStore()
        boat = Boat("Frygga", 0, "TiKi 26", 0.5, 0.5, 0.0)
        #store.addBoat(boat)
        gains = store.getGains(0)
        Kp = gains['proportional']
        Ki = gains['integral']
        Kd = gains['differential']
        print(Kp)
        print(Ki)
        print(Kd)
        pid = PidController(Kp,Ki,Kd)

        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch().decode('utf-8')
                print(f"Key pressed: {key}")
                if key == 'b':
                    store.getAllReadings()
                    store.dropAllTables()
                    break
            gps.update(power,timeConstant)
            heading = int(decoder.decode_Angle(gps.get_Current()))
            heading = round(heading)
            #print(heading)
            power = pid.pid(heading, target, dt)
            if power >= 90:
                power = 90
            elif power <= -90:
                power = -90
            print("power: ", power)
            visual.visualUpdate(heading, target)
            reading = Reading(0,0,heading, self.createTimeStamp())
            store.addReading(reading)
            target = updateTarget()
            time.sleep(dt)

    def createTimeStamp(self):
        return datetime.now().strftime('%H:%M:%S')


main = MainLoop()

thread1 = threading.Thread(target=run_flask, daemon=True)
thread2 = threading.Thread(target=main.main, daemon=True)

thread1.start()
thread2.start()

while True:
    time.sleep(1)