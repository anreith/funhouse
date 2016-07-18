'''
Created on Apr 6, 2014

@author: anreith
'''

import math
import pygame
import random
import operator
import engine.gameObject
import engine.world

class Energy():
    def __init__(self, src, dst, size, speed):
        self.dead = False
        self.src = src
        self.dst = dst
        self.size = size
        self.distanceTraveled = 0.0
        self.distanceTarget = src.getDistance(dst)
        self.speed = speed
        delta = map(operator.sub, dst.getPos(), src.getPos())
        self.angle = math.atan2(delta[1], delta[0])
        #print delta, self.angle, self.speed

    def getSize(self):
        return self.size

    def getSpeed(self):
        return self.speed

    def isDead(self):
        return self.dead

    def update(self, mSec):
        self.distanceTraveled += self.speed * mSec / 1000.0
        if self.distanceTraveled >= self.distanceTarget:
            #If we reached end of goal, add energy to destination tower and mark ourselves as dead
            self.dst.addEnergy(self.src, self.size, self.speed)
            self.dead = True

    def draw(self, surface):
        xpos = int(self.src.getPos()[0] + (math.cos(self.angle) * self.distanceTraveled))
        ypos = int(self.src.getPos()[1] + (math.sin(self.angle) * self.distanceTraveled))
        pygame.draw.circle(surface, (255,255,255), (xpos,ypos), self.size)

class Connection():
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst
        self.energy = []

    def addEnergy(self, size, speed):
        self.energy.append(Energy(self.src, self.dst, size, speed))

    def getSrc(self):
        return self.src

    def getDst(self):
        return self.dst

    def update(self, mSec):
        for e in self.energy:
            e.update(mSec)
        #Remove dead energy elements
        self.energy[:] = [x for x in self.energy if not x.isDead()]

    def draw(self, surface):
        pygame.draw.aaline(surface, (255,255,255), self.src.getPos(), self.dst.getPos(), True)

        for e in self.energy:
            e.draw(surface)


class Tower(engine.gameObject.GameObject):
    def __init__(self, data):
        engine.gameObject.GameObject.__init__(self, data)
        self.radius = data["radius"]
        self.cost = data["cost"]
        self.connections = []

    def clone(self):
        return Tower(self.data)

    def addConnection(self, dst):
        self.connections.append(Connection(self, dst))

    #Default policy is to relay energy to another tower
    def addEnergy(self, src, size, speed):
        if len(self.connections) == 0:
            print "Energy wasted at", self
        elif len(self.connections) == 1:
            self.connections[0].addEnergy(size, speed)
        #Choose a connection that is not connected to source
        else:
            candidates = [x for x in self.connections if not x.getDst() == src]
            candidates[random.randint(0, len(candidates) - 1)].addEnergy(size, speed)

    #Connect to other towers, return number of connections
    def connect(self):
        for other in engine.world.World().getTowers():
            if other.inRadius(self):
                self.addConnection(other)
                other.addConnection(self)
        return len(self.connections)

    def getRadius(self):
        return self.radius

    def getConnections(self):
        return self.connections[:]

    def getCost(self):
        return self.cost

    def inRadius(self, other):
        return self.getDistance(other) < max(self.radius, other.getRadius())

    def update(self, mSec):
        engine.gameObject.GameObject.update(self, mSec)
        for c in self.connections:
            c.update(mSec)

    def drawConnections(self, surface):
        for c in self.connections:
            c.draw(surface)
