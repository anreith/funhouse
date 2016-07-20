'''
Created on Apr 16, 2014

@author: anreith
'''

import sys
import os

import json
import tower
import suncatcherTower
import laserTower
import miningTower
import enemy
import ore
import animation

class ResHandler(object):
    #Borg/Monostate pattern
    __shared_state = {}
    def __init__(self):
        self.__dict__ = self.__shared_state
 
    def loadResources(self, mainResFile):
        self.animations = {}
        self.prototypes = {}
        self.levels = []
        self.currLevel = 0

        with open(mainResFile) as f:
            data = json.load(f)

            for animation in data["animations"]:
                self.addAnimation(animation)

            for resFile in data["prototypes"]:
                self.addPrototype(resFile)

            for levelFile in data["levels"]:
                self.levels.append(levelFile)
            
    def addPrototype(self, resFile):
        with open(resFile) as f:
            print(self, "Adding prototype from", resFile)

            data = json.load(f)
            type = data["type"]

            if type == "suncatcher":
                self.prototypes[type] = suncatcherTower.SuncatcherTower(data)
            elif type == "laser":
                self.prototypes[type] = laserTower.LaserTower(data)
            elif type == "miner":
                self.prototypes[type] = miningTower.MiningTower(data)
            elif type == "base":
                self.prototypes[type] = tower.Tower(data)
            elif type == "node":
                self.prototypes[type] = tower.Tower(data)
            elif type == "UFO":
                self.prototypes[type] = enemy.Enemy(data)
            elif type == "ore_small" or type == "ore_medium" or type == "ore_large":
                self.prototypes[type] = ore.Ore(data)
            else:
                print("Unknown prototype", type)

    def addAnimation(self, data):
        print(self, "Adding animation prototype", data["name"], "with gfx", data["gfx"])
        self.animations[data["name"]] = animation.Animation(data)

    def clone(self, goType, goPos):
        o = self.prototypes[goType].clone()
        o.setPos(goPos)
        return o

    def cloneAnimation(self, name, pos):
        a = self.animations[name].clone()
        a.setPos(pos)
        return a

    def getPrototype(self, type):
        return self.prototypes[type]

    def getNextLevel(self):
        if self.currLevel == len(self.levels):
            return None

        retVal = self.levels[self.currLevel]
        self.currLevel += 1
        return retVal
