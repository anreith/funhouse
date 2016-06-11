#!/usr/bin/python3

from PIL import Image, ImageDraw
from itertools import groupby

def loadAsGreyScale(imgfile):
  '''Load image and convert to greyscale'''
  image = Image.open(imgfile)
  image.convert('LA')
  return image

def chunkify(seq, size):
  '''Split sequence into chunks'''
  return [seq[pos:pos + size] for pos in range(0, len(seq), size)]

def getLines(image):
  '''Return image lines as array'''
  w, _ = image.size
  rawdata = list(image.getdata())
  lines = chunkify(rawdata, w)
  return lines

def isBlankLine(line):
  '''Return true if line is blank'''
  val = sum([v for v,_,_ in line])
  return val == 0

def getNonBlankBlocks(image):
  '''Enumerate/clump lines and return non-blank blocks'''
  #Save linenr and pixeldata 
  lines = [(nr, line) for nr,line in enumerate(getLines(image))]
  #Group lines into blank/non-blank blocks
  blocks = groupby(lines, lambda x: isBlankLine(x[1]))
  #Filter out blank line blocks
  blocks = [list(b[1]) for b in blocks if b[0] == False]
  return blocks

def lineStart(line):
  return next((i for i in range(0,len(line)) if line[i][0] != 0), len(line))

def lineStop(line):
  return len(line) - lineStart(list(reversed(line)))

def blockToRectangle(block):
  '''Create the smallest rectangle that would fit the line block'''
  starty = min([nr for nr,_ in block])
  stopy = max([nr for nr,_ in block])
  startx = min([lineStart(line) for _,line in block])
  stopx = max([lineStop(line) for _,line in block])

  #ATTN: fix
  starty -=1
  stopy +=1
  startx -=1
  stopx +=1

  return startx, starty, stopx, stopy

def drawRects(image, rects):
  draw = ImageDraw.Draw(image)
  for rect in rects:
    draw.rectangle(rect, outline=(255,0,0))

def saveAsRGB(image, filename):
  image.convert('RGB')
  image.save(filename)

im = loadAsGreyScale("../gfx/receipt/kvittotest03.png")

blocks = getNonBlankBlocks(im)

rects = [blockToRectangle(block) for block in blocks]
print(rects)

im2 = im.copy()
drawRects(im2, rects)
saveAsRGB(im2, "out.png")

im.show()
im2.show()
