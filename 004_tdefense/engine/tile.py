'''
Created on Mar 30, 2014

@author: anreith
'''

import pygame
import resHandler

class Tile(object):
    def __init__(self, data, pos):
        self.data = data
        self.pos = pos
        self.ani = resHandler.ResHandler().cloneAnimation(self.data["animation"], self.pos)
    
    def update(self, mSec):
        self.ani.update(mSec)

    def draw(self, surface):
        self.ani.draw(surface)
