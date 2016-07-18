'''
Created on Mar 30, 2014

@author: anreith
'''

import random
import math
import pygame
import json
import enemyWaveController
import resHandler
import tile

class World:
    #Borg/Monostate pattern
    __shared_state = {}
    def __init__(self):
        self.__dict__ = self.__shared_state

    def loadLevel(self, levelFile):
        self.width = 0
        self.height = 0
        self.tilemap = []
        self.tileset = []
        self.towertype = "none"
        self.levelFile = levelFile

        print "Loading level from %s" % (self.levelFile)

        with open(self.levelFile) as f:
            self.data = json.load(f)

        self.width = self.data["mapwidth"]
        self.height = self.data["mapheight"]
        self.twidth = self.data["tilewidth"]
        self.theight = self.data["tileheight"]
        self.ore = self.data["startore"]

        self.tiles = []
        self.enemies = []
        self.towers = []
        self.oredeposits = []

        self.__loadTiles()
        self.__loadOreDeposits()
        self.__loadTowers()
        self.__loadEnemies()

    def __loadTiles(self):
        tileset = self.data["tileset"]
        tilemap = self.data["tilemap"]
        
        for y in range(self.height):
            for x in range(self.width):
                tileValue = tilemap[y*self.width + x]
                self.tiles.append(tile.Tile(tileset[tileValue], [x*self.twidth, y*self.theight]))

    def __loadEnemies(self):
        #Add enemy wave controller
        self.enemyWaveController = enemyWaveController.EnemyWaveController(self.data["enemywaves"])
        
    def __loadTowers(self):
        #Add towers from levelfile, override need to be connected
        for tdata in self.data["towers"]:
            self.addTower(resHandler.ResHandler().clone(tdata["type"], tdata["pos"]), False)

    def __loadOreDeposits(self):
        for odata in self.data["oredeposits"]:
            self.addOreDeposit(resHandler.ResHandler().clone(odata["type"], odata["pos"]))

    #Add a tower, optionally refusing to add if not connected to existing tower
    def addTower(self, tower, requireConnect=True):
        nrConnections = tower.connect()
        if requireConnect and nrConnections == 0:
            print "Tower needs to connect to existing tower"
        else:
            self.towers.append(tower)
            tower.onSpawn()
            print self, "Added", tower.getType(), "tower at", tower.getPos()
            
    def addEnemy(self, enemy):
        self.enemies.append(enemy)
        enemy.onSpawn()

    def addOreDeposit(self, deposit):
        self.oredeposits.append(deposit)
        deposit.onSpawn()

    def addOre(self, amount):
        self.ore += amount
        print "ore:", self.ore

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
                print "Escape pressed, quitting"
                return False
            elif event.key == pygame.K_r:
                print "reloading '%s'" % self.levelFile
                self.loadLevel(self.levelFile)
            elif event.key == pygame.K_0:
                print "tower type none"
                self.towertype = "none"
            elif event.key == pygame.K_1:
                print "tower type node"
                self.towertype = "node"
            elif event.key == pygame.K_2:
                print "tower type suncatcher"
                self.towertype = "suncatcher"
            elif event.key == pygame.K_3:
                print "tower type laser"
                self.towertype = "laser"
            elif event.key == pygame.K_4:
                print "tower type miner"
                self.towertype = "miner"
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mpos = pygame.mouse.get_pos()
            
            if pygame.mouse.get_pressed() == (True, False, False) and self.towertype != "none":
                t = resHandler.ResHandler().clone(self.towertype, list(mpos))
                if t.getCost() > self.ore:
                    print "Not enough ore to build", t.getType(), "cost:", t.getCost(), "ore:", self.ore 
                else:
                    self.ore -= t.getCost()
                    print "Building", t.getType(), "cost:", t.getCost(), "ore remaining:", self.ore 
                    self.addTower(t)

            #Debug functionality: Create enemy at mouse position with base as target
            if pygame.mouse.get_pressed() == (False, False, True):
                self.addEnemy(resHandler.ResHandler().clone("UFO", list(mpos), self.getTowersByType("base")[0]))

        return True
