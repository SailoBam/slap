import sys
import os
import time
from boatDynamics.gpsSim import BoatSim as GpsSim
from nmea.nmeaDecoder import Decoder
from pid.pidModule import PidController
from visuals.liveCompass import Visual


class MainLoop:
    heading = 83
    timeConstant = 0.5
    dt = 0.01
    power = 0 
    target = 85
    # --- GAINS ---
    KP = -0.075
    KI = -0.1
    KD = 0.0

    gps = GpsSim()
    decoder = Decoder()
    pid = PidController(KP,KI,KD)
    visual = Visual(target)


    def main(self):
        while True:
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
            time.sleep(self.dt)

if __name__ == "__main__":
    main = MainLoop()
    main.main()