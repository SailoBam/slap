def angularDiff(a, b):
        c = b - a

        if c > 180:
            c = c - 360
        elif c < -180:
            c = c + 360
        return c