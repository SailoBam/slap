import math
import sys
import os

def iterate_Heading(heading, rudderAngle, timeConstant):
    k = 0
    #integrating constant
    # Preforms simple equation to iterate the heading and returns the output
    newHead = heading + rudderAngle * math.log(abs(timeConstant)) + k
    return newHead