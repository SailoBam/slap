import math
import sys
import os
def iterate_Heading(heading, rudderAngle, timeConstant):
    k = 0
    #integrating constant

    newHead = heading + rudderAngle * math.log(abs(timeConstant)) + k
    return newHead