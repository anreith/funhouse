'''
Created on Apr 10, 2014

@author: anreith
'''

import tower
import random
import pygame
import world

class LaserTower(tower.Tower):

    def __init__(self, data):
        tower.Tower.__init__(self, data)
        self.scanInterval = data["scaninterval"]
        self.attackRadius = data["attackradius"]
        self.energyOutput = data["energyoutput"] 
        self.target = None
        self.energyLevel = 0.0

    def onSpawn(self):
        self.setAnimation("laser_updown")

    def clone(self):
        return LaserTower(self.data)

    #Override base method, take energy for at least one second sustained fire (self.energyOutput)
    #If already at energy output level, default to routing behavior (in base class)
    def addEnergy(self, src, size, speed):
        if self.target and self.energyLevel < self.energyOutput:
            self.energyLevel += size
        else:
            tower.Tower.addEnergy(self, src, size, speed)

    def update(self, mSec):
        tower.Tower.update(self, mSec)

        if self.target:
            if self.target.isDead() or self.targetOutOfRange():
                self.scanForEnemies()
            elif self.energyLevel > 0:
                damage = min(self.energyLevel, self.energyOutput * mSec / 1000.0)
                actualDamage = self.target.registerHit(damage)
                self.energyLevel -= actualDamage
        else:
            if self.timeAccum > self.scanInterval:
                self.scanForEnemies()
                self.timeAccum %= self.scanInterval

    #Scan for enemies and choose a target if found
    def scanForEnemies(self):
        candidates = world.World().getEnemies()
        candidates = [x for x in candidates if self.getDistance(x) < self.attackRadius]
        if len(candidates) == 0:
            self.target = None
            self.color = (0,255,0)
        else:
            self.target = candidates[random.randint(0, len(candidates) - 1)]
            self.color = (255,0,0)

    def targetOutOfRange(self):
        return self.getDistance(self.target) > self.attackRadius

    def draw(self, surface):
        tower.Tower.draw(self, surface)
        if self.target and self.energyLevel > 0:
            pygame.draw.aaline(surface, (255,0,0), self.pos, self.target.getPos(), True)
