'''
Created on Apr 6, 2014

@author: anreith
'''

import sys
import os

import math
import pygame
import operator
import gameObject

class Enemy(gameObject.GameObject):
    def __init__(self, data):
        gameObject.GameObject.__init__(self, data)
        self.speed = data["speed"]
        self.attackRadius = data["attackradius"]
        self.target = None
        self.targetDistance = None
        self.angle = None

    def onSpawn(self):
        self.setAnimation("ufo")

    def clone(self):
        e = Enemy(self.data)
        return e

    def setTarget(self, target):
        self.target = target
        self.targetDistance =  self.target.getDistance(self)
        delta = list(map(operator.sub, self.getPos(), target.pos))
        self.angle = math.atan2(delta[1], delta[0])

    def update(self, mSec):
        gameObject.GameObject.update(self, mSec)
        if self.targetDistance > self.attackRadius:
            self.targetDistance -= self.speed * mSec / 1000.0
            xpos = self.target.getPos()[0] + (math.cos(self.angle) * self.targetDistance)
            ypos = self.target.getPos()[1] + (math.sin(self.angle) * self.targetDistance)
            self.setPos([int(xpos), int(ypos)])
