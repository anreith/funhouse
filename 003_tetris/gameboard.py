from itertools import chain

class Area:
  def __init__(self, w, h, ox=0, oy=0, fill=0):
    assert w > 0 and h > 0, "Width, height must be positive integers"

    self.w = w
    self.h = 0
    self.ox = ox
    self.oy = oy
    self.lines = []
    [self.addLine(y=0, fill=fill) for _ in range(0,h)]

  def getDimension(self):
    '''Return our dimensions'''
    return self.w, self.h

  def getOffset(self):
    '''Return our offset'''
    return self.ox, self.oy

  def getLine(self, y):
    '''return line value iterator'''
    assert not self.isPointOutside(0,y), "{} out of bounds".format(y)
    return iter(self.lines[y])

  def remLine(self, y):
    '''remove line'''
    assert not self.isPointOutside(0,y), "{} out of bounds".format(y)
    del self.lines[y]
    self.h -= 1

  def addLine(self, y, fill=0):
    '''Add empty line at y optionally filled'''
    assert y >= 0 and y <= self.h
    self.lines.insert(y, [fill] * self.w)
    self.h += 1

  def setVal(self, x, y, val):
    '''Set value at given coordinates'''
    assert not self.isPointOutside(x,y), "{},{} out of bounds".format(x,y)
    self.lines[y][x] = val

  def getVal(self, x, y):
    '''Get value at given coordinates'''
    assert not self.isPointOutside(x,y), "{},{} out of bounds".format(x,y)
    return self.lines[y][x]

  def getLinePoints(self, y):
    '''Return points on area line including offset'''
    return ((x+self.ox,y+self.oy, v) for x,v in enumerate(self.lines[y]) if v)

  def getPoints(self):
    '''Return points with value and optional translation'''
    return chain(*(self.getLinePoints(y) for y in range(0,self.h)))

  def isPointOutside(self, x,y):
    '''True if point is outside including offset'''
    rx = x - self.ox
    ry = y - self.oy
    return rx < 0 or rx >= self.w or ry < 0 or ry >= self.h

  def getOutsidePoints(self, other):
    '''Get points from other area that are outside this area'''
    return ((x,y,v) for x,y,v in other.getPoints() if self.isPointOutside(x,y))

  def getInsidePoints(self, other):
    '''Get points from other are that are inside this area'''
    return ((x,y,v) for x,y,v in other.getPoints() if not self.isPointOutside(x,y))

  def isOverLappedBy(self, other):
    '''True if other area points overlap points in this area'''
    return any(self.getVal(x,y) for x,y,_ in self.getInsidePoints(other))

  def __str__(self):
    strs = []
    for line in self.lines:
      strs.append("".join(str(v) for v in line))

    return "\n".join(strs)
