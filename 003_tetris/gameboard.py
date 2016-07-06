from itertools import chain

class Area:
  def __init__(self, w, h):
    assert w > 0 and h > 0, "Width, height must be positive integers"

    self.w = w
    self.h = 0
    self.lines = []
    [self.addLine(y=0, val=0) for _ in range(0,h)]

  def getDimension(self):
    return self.w, self.h

  def getLine(self, y):
    '''return iterator to line'''
    assert not self.isPointOutside(0,y), "{} out of bounds".format(y)
    return iter(self.lines[y])

  def remLine(self, y):
    assert not self.isPointOutside(0,y), "{} out of bounds".format(y)
    del self.lines[y]
    self.h -= 1

  def addLine(self, y, val):
    '''Add empty line at y'''
    assert y >= 0 and y <= self.h
    self.lines.insert(y, [val] * self.w)
    self.h += 1

  def setVal(self, x, y, val):
    assert not self.isPointOutside(x,y), "{},{} out of bounds".format(x,y)
    self.lines[y][x] = val

  def getVal(self, x, y):
    assert not self.isPointOutside(x,y), "{},{} out of bounds".format(x,y)
    return self.lines[y][x]

  def getLinePoints(self, y, dx=0, dy=0):
    '''Return points on a line that are non-empty with optional translation'''
    return ((x+dx,y+dy, v) for x,v in enumerate(self.lines[y]) if v)

  def getPoints(self, dx=0, dy=0):
    '''Return points with value and optional translation'''
    return chain(*(self.getLinePoints(y, dx, dy) for y in range(0,self.h)))

  def isPointOutside(self, x,y):
    return x < 0 or x >= self.w or y < 0 or y >= self.h

  def getOutsidePoints(self, other, dx=0, dy=0):
    return ((x,y,v) for x,y,v in other.getPoints(dx, dy) if self.isPointOutside(x,y))

  def getInsidePoints(self, other, dx=0, dy=0):
    return ((x,y,v) for x,y,v in other.getPoints(dx, dy) if not self.isPointInside(x,y))

  def isOverLappedBy(self, other, dx, dy):
    return any(self.getVal(x,y) for x,y,_ in getInsideBoundsPoints(self, other, dx, dy))

  def __str__(self):
    strs = []
    for line in self.lines:
      strs.append("".join(str(v) for v in line))

    return "\n".join(strs)
