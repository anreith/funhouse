'''
Created on Mar 30, 2014

@author: anreith
'''


import json
import math
import os
import random
import sys
import pygame

import enemyWaveController
import resHandler
import tile

class World:
    #Borg/Monostate pattern
    __shared_state = {}
    def __init__(self):
        self.__dict__ = self.__shared_state

    def loadLevel(self, levelFile):
        self.tilemap = []
        self.tileset = []
        self.towertype = "none"
        self.levelFile = levelFile

        print("Loading level from '{}'".format(self.levelFile))

        with open(self.levelFile) as f:
            self.data = json.load(f)

        self.mapdim = (self.data["mapdim"]["w"], self.data["mapdim"]["h"])
        self.tiledim = (self.data["tiledim"]["w"], self.data["tiledim"]["h"])
        self.startPoint = (self.data["start"]["x"] * self.tiledim[0], self.data["start"]["y"] * self.tiledim[1])
        self.ore = self.data["startore"]
        self.enemyWaveController = enemyWaveController.EnemyWaveController(self.data["enemywaves"])
        self.towers = list(map(resHandler.ResHandler().clone, self.data["towers"]))

    def getTiles(self):
        return iter(self.data["tilemap"])

    def getWidth(self):
        return self.data["mapdim"]["w"]

    def getHeight(self):
        return self.data["mapdim"]["h"]

    def getWaypoints(self):
        return iter(self.data["waypoints"])

    def getStartX(self):
        return self.data["startpoint"]["x"]

    def getStartY(self):
        return self.data["startpoint"]["y"]

    def addTower(self, tower):
        self.towers.append(tower)
        tower.onSpawn()
        print("{} Added {} tower at {}".format(self, tower.getType(), tower.getPos()))
            
    def addEnemy(self, enemy):
        self.enemies.append(enemy)
        enemy.onSpawn()

    def addOreDeposit(self, deposit):
        self.oredeposits.append(deposit)
        deposit.onSpawn()

    def addOre(self, amount):
        self.ore += amount
        print("ore: {}".format(self.ore))

    def getTowers(self):
        return self.towers[:]

    def getTowersByType(self, type):
        return [x for x in self.towers if x.getType() == type][:]

    def getEnemies(self):
        return self.enemies[:]

    def getOreDeposits(self):
        return self.oredeposits[:]

    def update(self, mSec):
        for tile in self.tiles:
            tile.update(mSec)
            
        for tower in self.towers:
            tower.update(mSec)

        for enemy in self.enemies:
            enemy.update(mSec)

        if not self.enemyWaveController.done():
            self.enemyWaveController.update(mSec)

        for deposit in self.oredeposits:
            deposit.update(mSec)

        self.enemies = [e for e in self.enemies if not e.isDead()]
        self.towers = [t for t in self.towers if not t.isDead()]
        self.oredeposits = [o for o in self.oredeposits if not o.isDead()]

    def draw(self, surface):
        for tile in self.tiles:
            tile.draw(surface)
        
        for deposit in self.oredeposits:
            deposit.draw(surface)

        #Draw tower connections before towers
        for tower in self.towers:
            tower.drawConnections(surface)

        for tower in self.towers:
            tower.draw(surface)

        for enemy in self.enemies:
            enemy.draw(surface)

        if self.towertype != "none":
            t = resHandler.ResHandler().getPrototype(self.towertype)
            pygame.draw.circle(surface, t.getColor(), pygame.mouse.get_pos(), t.getRadius(), 1)

        spawnRadius = self.enemyWaveController.getCurrentWaveSpawnRadius()
        baseTower = self.getTowersByType("base")[0]
        pygame.draw.circle(surface, (255,255,255), tuple(baseTower.getPos()), spawnRadius, 1)
        
    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print("Escape pressed, quitting")
                return False
            elif event.key == pygame.K_r:
                print("reloading '{}'".format(self.levelFile))
                self.loadLevel(self.levelFile)
            elif event.key == pygame.K_0:
                print("tower type none")
                self.towertype = "none"
            elif event.key == pygame.K_1:
                print("tower type node")
                self.towertype = "node"
            elif event.key == pygame.K_2:
                print("tower type suncatcher")
                self.towertype = "suncatcher"
            elif event.key == pygame.K_3:
                print("tower type laser")
                self.towertype = "laser"
            elif event.key == pygame.K_4:
                print("tower type miner")
                self.towertype = "miner"
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mpos = pygame.mouse.get_pos()
            
            if pygame.mouse.get_pressed() == (True, False, False) and self.towertype != "none":
                t = resHandler.ResHandler().clone(self.towertype, list(mpos))
                if t.getCost() > self.ore:
                    print("Not enough ore to build", t.getType(), "cost:", t.getCost(), "ore:", self.ore)
                else:
                    self.ore -= t.getCost()
                    print("Building", t.getType(), "cost:", t.getCost(), "ore remaining:", self.ore)
                    self.addTower(t)

            #Debug functionality: Create enemy at mouse position with base as target
            if pygame.mouse.get_pressed() == (False, False, True):
                self.addEnemy(resHandler.ResHandler().clone("UFO", list(mpos), self.getTowersByType("base")[0]))

        return True
