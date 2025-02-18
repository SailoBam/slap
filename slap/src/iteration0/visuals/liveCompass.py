import turtle
import time
import msvcrt

class Visual:

    wn = turtle.Screen()


    def __init__(self, targetAngle):
        rectangle = ((0, -1), (100, -1), (100, 1), (0, 1))
        turtle.register_shape("thin_rect", rectangle)

        self.point = turtle.Turtle()
        marker = turtle.Turtle()
        marker.color("red")
        marker.setheading(targetAngle - 90)
        marker.pendown()
        marker.pensize(3)
        marker.forward(100)
        marker.hideturtle()
        self.point.shape("thin_rect")
        self.point.penup()

        self.point.speed(10000000000000000000000000000)
        self.point.color("black")

    def visualUpdate(self, currentAngle):
        self.point.setheading(currentAngle)
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
        