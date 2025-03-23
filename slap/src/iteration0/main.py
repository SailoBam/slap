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
class MainLoop:
    heading = 83
    timeConstant = 0.5
    dt = 0.01
    power = 0 
    target = 85
    # --- GAINS ---
    KP = 0.0
    KI = 0.0
    KD = 0.0

    gps = GpsSim()
    decoder = Decoder()
    
    visual = Visual(target)
    store = SlapStore()
    boat = Boat("Frygga", 0, "Tiki 26", 0.075, 0.1, 0.0)
    store.addBoat(boat)
    def main(self):
        gains = self.store.getGains(0)
        self.KP = gains['proportional']
        self.KI = gains['integral']
        self.KD = gains['differential']
        print(self.KP)
        print(self.KI)
        print(self.KD)
        self.pid = PidController(self.KP,self.KI,self.KD)
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch().decode('utf-8')
                print(f"Key pressed: {key}")
                if key == 'b':
                    self.store.getAllReadings()
                    break
            self.gps.update(self.power,self.timeConstant)

            self.heading = int(self.decoder.decode_Angle(self.gps.get_Current()))
            self.heading = round(self.heading)
            print(self.heading)
            self.power = self.pid.pid(self.heading, self.target, self.dt)
            if self.power >= 90:
                self.power = 90
            elif self.power <= -90:
                self.power = -90
            self.visual.visualUpdate(int(self.decoder.decode_Angle(self.gps.get_Current())))
            reading = Reading(0,0,self.heading, self.createTimeStamp())
            self.store.addReading(reading)
            time.sleep(self.dt)

    def createTimeStamp(self):
        return datetime.now().strftime('%H:%M:%S')

if __name__ == "__main__":
    main = MainLoop()
    main.main()
    