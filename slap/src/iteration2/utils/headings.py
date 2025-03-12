def angularDiff(a, b):
        c = b - a

        if c > 180:
            c = c - 360
        elif c < -180:
            c = c + 360
        return c

def compassify(input):
    print("Compassing: ", input)
    
    return input% 360