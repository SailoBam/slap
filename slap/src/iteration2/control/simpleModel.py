import math
import sys
import os

def iterate_Heading(heading, rudderAngle, timeConstant):
    k = 0
    #integrating constant
    # Preforms simple equation to iterate the heading and returns the output
    
    newHead = heading + rudderAngle / 10
    #newHead = heading + rudderAngle * math.log(abs(timeConstant)) + k
    return newHead

'''
The code here is for the first order differential equation which is a better model of the boat behavour.
TODO: Fix up first order maths and put code here to make a more realistic boat simulator
'''