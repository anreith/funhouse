class Board():
    '''The Board class represents a simple game board with width and height
       The methods allow the getting and setting of values from/to the board
       Bounds checking is not performed.
    '''

    def __init__(self, width, height, allowed=[], clearval=None):
        '''Initialize a board with width, height, allowed values and clear value
           Also clears the board
        '''
        self.width = width
        self.height = height
        self.clearval = clearval
        self.allowed = allowed
        self.clearAll()

    def isWithinBounds(self, x, y):
        '''Check if given coordinates are within bounds'''
        assert isinstance(x, int) and isinstance(y, int), "Coordinates should be integers"
        return x >= 0 and x < self.width and y >= 0 and y < self.height

    def isAllowed(self, v):
        '''Check if given value is allowed on the board'''
        return not self.allowed or v in self.allowed

    def getData(self):
        '''Return raw board data'''
        return self.data[:]

    def get(self, x, y):
        '''Get board value from coordinates'''
        assert self.isWithinBounds(x,y), "Coordinates need to be bound-checked"
        return self.data[y * self.width + x]

    def set(self, x, y, v):
        '''Set board value on coordinates'''
        assert self.isWithinBounds(x,y), "Coordinates need to be bound-checked"
        if self.isAllowed(v):
            self.data[y * self.width + x] = v
            return True

        return False

    def isClear(self, x, y):
        '''Check if board coordinate is cleared'''
        assert self.isWithinBounds(x,y), "Coordinates need to be bound-checked"
        return self.get(x,y) == self.clearval
        
    def clear(self, x, y):
        '''Clear board coordinates'''
        assert self.isWithinBounds(x,y), "Coordinates need to be bound-checked"
        self.data[y * self.width + x] = self.clearval
        return True

    def clearAll(self):
        '''Clear entire board'''
        self.data = [self.clearval] * self.width * self.height
