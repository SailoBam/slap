from simpleModel import iterate_Heading as tick
import msvcrt

heading = 32
rudderAngle = 5

if __name__ == "__main__":
    temp = tick(heading, 45)
    print("This is your current heading: ")
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch().decode('utf-8')
            if key == 'a':
                temp = tick(temp, rudderAngle, 0.5)
            elif key == 'd':
                temp = tick(temp, -rudderAngle, 0.5)

            if temp >= 360:
                temp = temp - 360
            elif temp < 0:
                temp = 360 + temp
            print(temp)

        