__doc__ = '''Keyboard module with keyboard input convenience functions'''

def get_tuple_int(minx, miny, maxx, maxy, delimiter=','):
    '''Get int tuple separated by delimiter'''
    x,y = tuple(int(x.strip()) for x in input().split(delimiter))
    while x < minx or x > maxx or y < miny or y > maxy:
        print("Input out of bounds ({},{})-({},{}), insert again:".format(minx, miny, maxx, maxy))
        x,y = tuple(int(x.strip()) for x in input().split(','))

    return x,y

