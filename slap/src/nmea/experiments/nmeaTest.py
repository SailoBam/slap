from nmeaEncoder import Encoder, encode_Position
from nmeaEncoder import encode_Angle
from simpleNmea import Nmea
import unittest
import datetime

class TestStringMethods(unittest.TestCase):
    

    def test_Angle(self):
        parser = Nmea()
        self.assertEqual(parser.get_Angle(encode_Angle()), correctAngle)

    def test_Position(self):
        parser = Nmea()
        positionTemp = parser.get_Pos(encode_Position())
        position = [positionTemp[1], positionTemp[2]]
        self.assertEqual(position, correctPosition)


now = datetime.datetime.now()
time = str(now.time())
timeList = time.split(":")
formattedTime = [timeList[0] + "h" + timeList[1] + "m" + timeList[2][:2] + "s"]
time = "".join(formattedTime)

correctAngle = 102.24

correctPosition = ["10N", "50W"]
print(correctPosition)



        
        
if __name__ == "__main__":
    unittest.main()