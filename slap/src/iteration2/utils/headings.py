def angularDiff(a, b):
        c = b - a

        if c > 180:
            c = c - 360
        elif c < -180:
            c = c + 360
        return c

def compassify(input):
    print("Compassing: ", input)
    if input == 360:
        output = 0
    elif input > 360:
        output = input - 360
    elif input < 0:
        output = 360 + input
    else:
        output = input
    return output