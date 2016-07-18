'''
Created on Apr 13, 2014

@author: anreith
'''

import pygame
import math
import operator
import resHandler
import animation

class GameObject(object):
    def __init__(self, data):
        self.dead = False
        self.data = data
        self.type = data["type"]
        self.hp = float(data["hp"])
        self.color = tuple(data["color"])
        self.pos = [0,0]
        self.timeAccum = 0.0
        self.animations = {}
        self.currAnimation = None
        #Load animations
        for aName in data["animations"]:
            self.animations[aName] = resHandler.ResHandler().cloneAnimation(aName, [0,0])

    #Override this to implement behaviour when spawning
    def onSpawn(self):
        pass

    def setPos(self, pos):
        self.pos = pos[:]
        
        for animation in self.animations.values():
            animation.setPos(self.pos)

    #Register damage and return actual damage done
    def registerHit(self, damage):
        retVal = min(self.hp, damage)
        self.hp -= damage
        return retVal

    def setAnimation(self, aName):
        self.currAnimation = self.animations[aName]

    def getType(self):
        return self.type

    def getPos(self):
        return self.pos[:]

    def getColor(self):
        return self.color

    def getDistance(self, other):
        return math.sqrt(sum([x**2 for x in map(operator.sub, self.pos, other.getPos())]))

    def isDead(self):
        return self.hp <= 0.0

    def update(self, mSec):
        self.timeAccum += mSec / 1000.0

        if self.currAnimation:
            self.currAnimation.update(mSec)

    def draw(self, surface):
        if self.currAnimation:
            self.currAnimation.draw(surface)
            pygame.draw.circle(surface, self.color, tuple(self.pos), 2)
        else:
            pygame.draw.circle(surface, self.color, tuple(self.pos), 10)
