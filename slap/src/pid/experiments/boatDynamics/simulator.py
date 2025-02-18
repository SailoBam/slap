from simpleModel import iterate_Heading as iterate
import msvcrt

class BoatSim:

    heading = 0

    def update(self, power, timeConstant):
        rudderAngle = power * (1 / 360)
        self.heading = iterate(self.heading, rudderAngle, timeConstant)
        self.heading = round(self.heading)
        #self.create_Angle_String(self.heading)

    
    def get_Current(self):
        return self.heading
    
    def create_Angle_String(self,input):
        code = ["$--HDT"]
        code.append(input)
        code.append("T")
        strCode = ""
        for i in range(0,len(code)):
            if i != 0:
                strCode = strCode + ","
            strCode = strCode + code[i]
        return strCode

if __name__ == "__main__":
    simulator = BoatSim()
    while True:
        simulator.update(50, 0.5)