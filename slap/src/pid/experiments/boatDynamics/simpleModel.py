import math
def iterate_Heading(heading, rudderAngle):
    T = 0.5
    #Time constant
    k = 0
    #intergrating constant

    newHead = heading + rudderAngle * math.log(abs(T)) + k
    return newHead