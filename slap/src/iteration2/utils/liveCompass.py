import turtle
import time
import msvcrt

class Visual:


    def __init__(self, targetAngle):
        wn = turtle.Screen()
        rectangle = ((0, -1), (100, -1), (100, 1), (0, 1))
        turtle.register_shape("thin_rect", rectangle)

        self.point = turtle.Turtle()
        self.marker = turtle.Turtle()
        self.marker.color("red")
        self.marker.shape("thin_rect")
        self.point.shape("thin_rect")
        self.point.penup()

        self.point.speed(10000000000000000000000000000)
        self.point.color("black")

    def visualUpdate(self, currentAngle, target):
        self.point.setheading(currentAngle)
        self.marker.setheading(target)

        
if __name__ == "__main__":
    visual = Visual(60)
    angle = 0
    while True:
        if msvcrt.kbhit():  # Check if a key was pressed
            key = msvcrt.getch().decode('utf-8')  # Get the key
            print(f"Key pressed: {key}")
            if key == 'a':  # Exit condition
                angle = angle + 10
            elif key == 'd':
                angle = angle - 10
        visual.visualUpdate(angle)
        