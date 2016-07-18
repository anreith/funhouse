'''
Created on Apr 12, 2014

@author: anreith
'''

import random
import math
import world
import resHandler

class EnemyWave(object):
    def __init__(self, data):
        self.spawnRadius = data["spawnradius"]
        self.spawnInterval = data["spawninterval"]
        self.enemyType = data["enemytype"]
        self.enemyCount = data["enemycount"]
        self.targetType = data["targettype"]
        self.spawnedEnemies = 0
        self.timeAccum = 0.0
        self.enemies = []

    def update(self, mSec):
        self.timeAccum += mSec / 1000.0
        while self.timeAccum > self.spawnInterval and self.spawnedEnemies < self.enemyCount:
            self.spawnEnemy()
            self.spawnedEnemies += 1
            self.timeAccum -= self.spawnInterval

        self.enemies = [x for x in self.enemies if not x.isDead()]

    def spawnEnemy(self):
        candidateTargets = world.World().getTowersByType(self.targetType)
        assert len(candidateTargets) > 0, "No candidate targets for enemy"

        target = candidateTargets[random.randint(0, len(candidateTargets) - 1)]
        tpos = target.getPos()
        angle = random.uniform(0, math.pi * 2.0)
        x = tpos[0] + math.cos(angle) * self.spawnRadius
        y = tpos[1] + math.sin(angle) * self.spawnRadius
        
        e = resHandler.ResHandler().clone(self.enemyType, [int(x),int(y)])
        e.setTarget(target)
        world.World().addEnemy(e)
        self.enemies.append(e)

    def getSpawnRadius(self):
        return self.spawnRadius

    #check if all enemies are spawned and dead
    def done(self):
        return self.spawnedEnemies >= self.enemyCount and len(self.enemies) == 0 


class EnemyWaveController(object):
    def __init__(self, data):
        self.data = data
        self.currentWave = None
        self.waveNr = 0

        assert len(self.data) > 0, "No waves configured"
        self.startWave(self.waveNr)

    def startWave(self, waveNr):
        print self, "starting wave", waveNr
        self.currentWave = EnemyWave(self.data[self.waveNr])

    def update(self, mSec):
        self.currentWave.update(mSec)
        if self.currentWave.done() and not self.done():
            self.waveNr += 1
            self.startWave(self.waveNr)

    def currentWaveNr(self):
        return self.waveNr

    def getCurrentWaveSpawnRadius(self):
        return self.currentWave.getSpawnRadius()

    def done(self):
        return self.currentWave.done() and self.waveNr + 1 == len(self.data) 
