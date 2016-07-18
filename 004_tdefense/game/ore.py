'''
Created on Apr 6, 2014

@author: anreith
'''

import pygame
import engine.gameObject

class Ore(engine.gameObject.GameObject):
    def __init__(self, data):
        engine.gameObject.GameObject.__init__(self, data)

    def clone(self):
        o = Ore(self.data)
        return o

    def onSpawn(self):
        #Set animation corresponding to size; ore_small/ore_medium/ore_large
        self.setAnimation(self.type)
