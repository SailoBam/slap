import turtle
import time

class Visual:

    wn = turtle.Screen()

    def __init__(self):
        MARK_X = 15
        MARK_Y = 0
        marker = turtle.Turtle()
        marker.color("red")
        marker.speed(1000)
        marker.goto(-1000,MARK_Y)
        marker.goto(1000,MARK_Y)
        marker.goto(MARK_X,MARK_Y)
        marker.penup()
        marker.goto(MARK_X,MARK_Y)
        marker.right(180)
        self.point = turtle.Turtle()
        self.point.penup()
        self.point.shape("square")
        self.point.color("black")
        self.point.right(90)

    def visual(self,pos):
            self.point.goto(0,pos)


