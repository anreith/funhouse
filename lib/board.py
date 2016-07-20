from itertools import groupby, product

__doc__ = '''File contains board abstraction class and helper functions'''

def in_a_row(gameboard, inarow):
    '''Get all values with number of elements in a row'''
    retval = []
    clearval = gameboard.clearVal()
    for row in gameboard.getRows():
        retval.extend([v for v,n in groupby(row) if v != clearval and len(list(n)) >= inarow])

    for col in gameboard.getColumns():
        retval.extend([v for v,n in groupby(col) if v != clearval and len(list(n)) >= inarow])

    return retval

class Board():
    '''The Board class represents a simple game board with width and height
       The methods allow the getting and setting of values from/to the board
    '''

    def __init__(self, dim, allowed=[], clearval=None, data=None):
        '''Initialize a board with width, height, allowed values and clear value
           Also clears the board
        '''
        self.w, self.h = dim
        self.clearval = clearval
        self.allowed = allowed
        if data:
            assert len(data) == len(self), "Dimension/Data mismatch"
            self.data = data
        else:
            self.clearAll()

    def size(self):
        '''Return size of gameboard as tuple'''
        return self.w, self.h

    def __len__(self):
        '''Return number of game board spaces'''
        return self.w * self.h

    def __iter__(self):
        '''Iterate through board data'''
        return iter(self.data)

    def isWithinBounds(self, x, y):
        '''Check if given coordinates are within bounds'''
        return x >= 0 and x < self.w and y >= 0 and y < self.h

    def isAllowed(self, v):
        '''Check if given value is allowed on the board'''
        return not self.allowed or v in self.allowed

    def getRows(self):
        '''Return horisontal rows of board data'''
        return (self.data[i:i + self.w] for i in range(0, len(self), self.w))

    def getColumns(self):
        '''Return vertical rows of board data'''
        rows = list(self.getRows())
        return (list(c) for c in zip(*rows[::1])) #Rotate list

    def getCoordData(self):
        '''Get data prefixed with coordinates'''
        return zip(product(range(0, self.w), range(0, self.h)), iter(self))

    def getValue(self, x, y):
        '''Get board value from coordinates'''
        assert self.isWithinBounds(x,y), "Coordinates need to be bound-checked"
        return self.data[y * self.w + x]

    def setValue(self, x, y, v):
        '''Set board value on coordinates'''
        assert self.isWithinBounds(x,y), "Coordinates need to be bound-checked"
        assert self.isAllowed(v), "Value not allowed"
        self.data[y * self.w + x] = v

    def isClear(self, x, y):
        '''Check if board coordinate is cleared'''
        assert self.isWithinBounds(x,y), "Coordinates need to be bound-checked"
        return self.getValue(x,y) == self.clearval
        
    def clear(self, x, y):
        '''Clear board coordinates'''
        assert self.isWithinBounds(x,y), "Coordinates need to be bound-checked"
        self.data[y * self.w + x] = self.clearval
        return True

    def clearAll(self, clearval=None):
        '''Clear entire board'''
        clearval = clearval or self.clearval
        self.data = [clearval] * len(self)

    def getClearVal(self):
        '''Return clear value'''
        return self.clearval

    def isFilled(self):
        '''True if no clear coordinates on board'''
        return not self.clearval in self.data

    def print(gameboard):
        '''Naive print of gameboard'''
        for row in gameboard.getRows():
            print("".join(row))
