
#from ascii import isdigit


class Nmea:

    def get_Pos(self, nmeaCode):
        # Example string:
        # $GPGGA,hhmmss.ss,llll.ll,a,yyyyy.yy,a,x,xx,x.x,x.x,M,x.x,M,x.x,xxxx

        # Key:
        #hhmmss.ss = UTC of position
        #llll.ll = latitude of position
        #a = N or S
        #yyyyy.yy = Longitude of position
        #a = E or W
        #x = GPS Quality indicator (0=no fix, 1=GPS fix, 2=Dif. GPS fix)
        #xx = number of satellites in use
        #x.x = horizontal dilution of precision
        #x.x = Antenna altitude above mean-sea-level
        #M = units of antenna altitude, meters
        #x.x = Geoidal separation
        #M = units of geoidal separation, meters
        #x.x = Age of Differential GPS data (seconds)
        #xxxx = Differential reference station ID

        #nmeaList = nmeaCode.split(",")
        print(nmeaCode)
        nmeaList = nmeaCode
        time = nmeaList[0]
        # time = time[:2] + 'h' + time[2:4] + 'm' + time[4:6] + 's'
        lat = nmeaList[1]
        long = nmeaList[2]
        pos = [time,lat,long]
        return pos
    
    def get_Angle(self, nmeaCode):
        listCode = nmeaCode.split(',')
        angle_str = listCode[1]
        angle = float(angle_str)
        print(angle)
        return angle