#!/usr/bin/python3

from PIL import Image
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
  _, w = image.size
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
  blocks = [b[1] for b in blocks if b[0] == False]
  return blocks

im = loadAsGreyScale("../gfx/receipt/kvittotest01.png")

blocks = getNonBlankBlocks(im)
print(blocks)
im.show()
