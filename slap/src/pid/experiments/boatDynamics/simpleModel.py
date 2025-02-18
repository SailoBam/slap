import math
def iterate_Heading(heading, rudderAngle, timeConstant):
    k = 0
    #intergrating constant

    newHead = heading + rudderAngle * math.log(abs(timeConstant)) + k
    return newHead