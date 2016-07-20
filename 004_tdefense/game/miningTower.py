'''
Created on Apr 19, 2014

@author: anreith
'''

import tower
import world
import pygame
import random

class MiningTower(tower.Tower):

    def __init__(self, data):
        tower.Tower.__init__(self, data)
        self.mineRadius = data["mineradius"]
        self.dumpInterval = data["dumpinterval"]
        self.energyOutput = data["energyoutput"] 
        self.conversionRate = data["conversionrate"]
        self.target = None
        self.energyLevel = 0.0
        self.oreStorage = 0.0

    #When spawned, start mining immediately
    def onSpawn(self):        
        self.scanForOre()

    def clone(self):
        return MiningTower(self.data)

    #Override base method, take energy for at least one second sustained mining (self.energyOutput)
    #If already at energy output level, default to routing behavior (in base class)
    def addEnergy(self, src, size, speed):
        if self.target and self.energyLevel < self.energyOutput:
            self.energyLevel += size
        else:
            tower.Tower.addEnergy(self, src, size, speed)

    def update(self, mSec):
        tower.Tower.update(self, mSec)

        if self.target:
            if self.target.isDead():
                self.scanForOre()
            elif self.energyLevel > 0:
                #Ore is implemented as a GameObject, so mining == shooting
                damage = min(self.energyLevel, self.energyOutput * mSec / 1000.0)
                actualDamage = self.target.registerHit(damage)
                self.energyLevel -= actualDamage
                self.oreStorage += actualDamage * self.conversionRate

        if self.timeAccum > self.dumpInterval:
            if self.oreStorage > 0:
                world.World().addOre(self.oreStorage)
                self.oreStorage = 0
            self.timeAccum %= self.dumpInterval

    #Scan for enemies and choose a target if found
    def scanForOre(self):
        candidates = world.World().getOreDeposits()

        for c in candidates:
            print(c.getPos(), self.getDistance(c), self.mineRadius)

        candidates = [x for x in candidates if self.getDistance(x) < self.mineRadius]
        if len(candidates) == 0:
            self.target = None
            self.color = (255,128,255)
        else:
            self.target = candidates[random.randint(0, len(candidates) - 1)]
            self.color = (255,0,255)

    def draw(self, surface):
        tower.Tower.draw(self, surface)
        if self.target and self.energyLevel > 0:
            pygame.draw.aaline(surface, (255,0,255), self.pos, self.target.getPos(), True)
