from simpleModel import iterate_Heading as tick
import msvcrt

heading = 32
rudderAngle = 5

if __name__ == "__main__":
    temp = tick(heading, 45)
    print("This is your current heading: ")
    while True:
        if msvcrt.kbhit():  # Check if a key was pressed
            key = msvcrt.getch().decode('utf-8')  # Get the key
            print(f"Key pressed: {key}")
            if key == 'a':  # Exit condition
                temp = tick(temp, rudderAngle)
            elif key == 'd':
                temp = tick(temp, -rudderAngle)

            if temp >= 360:
                temp = temp - 360
            elif temp <= -360:
                temp = temp + 360
            print(temp)

        