import datetime
 
class Encoder:

    def get_Input(self):
        inputStr = input("Enter the desired value ")
        return inputStr
    
    def get_Pos(self):
        print("latitude: ")
        latitude = (self.get_Input() + input("Enter N or S "))
        print("Longitude: ")
        longitude = (self.get_Input() + input("Enter W or E "))
        now = datetime.datetime.now()

        time = str(now.time())
        timeList = time.split(":")
        formattedTime = [timeList[0] + "h" + timeList[1] + "m" + timeList[2][:2] + "s"]
        time = "".join(formattedTime)
        inputList = [time, latitude, longitude, 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']
        return inputList

    
    
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
    
    def create_Pos_String(self,input):
        code = ["$--GGA"]
        for i in range(0, len(input)):
            code.append(input[i])
        #print(code)

def encode_Angle():
    encode = Encoder()
    input = encode.get_Input()
    output = encode.create_Angle_String(input)
    return output

def encode_Position():
    encode = Encoder()
    output = encode.get_Pos()
    return output


if __name__ == "__main__":
    encode_Position()