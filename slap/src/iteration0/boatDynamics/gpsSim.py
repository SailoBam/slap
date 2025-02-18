from .simpleModel import iterate_Heading as iterate
import msvcrt
import sys
import os
class BoatSim:

    heading = 0

    def update(self, power, timeConstant):
        #rudderAngle = (power / 360)
        rudderAngle = -power
        self.heading = iterate(self.heading, rudderAngle, timeConstant)
        self.heading = round(self.heading)
        if self.heading >= 360:
            self.heading = self.heading - 360
        elif self.heading <= 0:
            self.heading = 360 + self.heading
       
    
    def get_Current(self):
        heading = self.create_Angle_String(self.heading)

        return heading
    
    def create_Angle_String(self,input):
        code = ["$--HDT"]
        code.append(input)
        code.append("T")
        strCode = ""
        for i in range(0,len(code)):
            if i != 0:
                strCode = strCode + ","
            strCode = strCode + str(code[i])
        return strCode

if __name__ == "__main__":
    simulator = BoatSim()
    while True:
        simulator.update(1, 0.5)
        print(simulator.get_Current())