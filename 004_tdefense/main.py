'''
Created on Mar 30, 2014

@author: anreith
'''

import os
import sys
import pygame

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/engine")
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/game")

print(sys.path)

import world
import resHandler

levelFile = "res/lvl/01.json"

if len(sys.argv) == 3:
    resFile = sys.argv[1]
    levelFile = sys.argv[2]

pygame.init() 
screen = pygame.display.set_mode((1024, 768)) 
framerate = 60

#Load all resources
resHandler.ResHandler().loadResources("res/res.json")

print("Loading level '{}'".format(levelFile))
world.World().loadLevel(resHandler.ResHandler().getNextLevel())

clock = pygame.time.Clock()
totalTime = 0

runGame = True
while runGame: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            runGame = False
        else:
            #Allow world to quit game
            runGame = world.World().handleEvent(event)

    mSec = clock.tick(framerate)

    totalTime += mSec
    if(totalTime > 5000):
        print(clock.get_fps())
        totalTime %= 5000 

#    screen.fill((0,0,0))
    world.World().update(mSec)
    world.World().draw(screen)
    pygame.display.flip()
