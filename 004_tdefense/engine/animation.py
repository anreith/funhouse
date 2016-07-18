'''
Created on Apr 18, 2014

@author: anreith
'''

import resHandler
import pygame
import operator

class Animation(object):
    def __init__(self, data, gfx=None):
        self.data = data
        self.name = data["name"]
        #Load gfx only once for multiple instances of cloned animations
        self.gfx = gfx if gfx else self.__loadGfx(data["gfx"])
        self.offset = data["offset"]
        self.nrFrames = data["frames"]
        self.paused = True
        
        self.currFrame = 0
        self.timeAccum = 0.0
        self.setPos([0,0])

        #No point in providing/setting duration or framesize for stills
        if self.nrFrames > 1:
            self.frameDuration = float(data["duration"]) / self.nrFrames
            w = self.gfx.get_width();
            h = self.gfx.get_height();
            assert w % self.nrFrames == 0, "'%s' width %d not evenly divisible into %d frames" % (data["gfx"], w, self.nrFrames) 
            self.frameSize = (w / self.nrFrames, h)
            self.srcRect = pygame.Rect((0,0), self.frameSize)
            
            self.paused = data["paused"]


    def __loadGfx(self, gfxFile):
        gfx = pygame.image.load(gfxFile)
        if gfx.get_alpha():
            gfx = gfx.convert_alpha()
        else:
            gfx = gfx.convert()
        
        return gfx

    def clone(self):
        return Animation(self.data, self.gfx)

    def setPos(self, pos):
        self.pos = map(operator.sub, pos[:], self.offset)
        
    def nextFrame(self):
        if not self.isDone():
            self.currFrame += 1
            self.srcRect.move_ip(self.frameSize[0], 0)

    def getFrameSize(self):
        return self.frameSize
    
    def isDone(self):
        return self.currFrame >= self.nrFrames - 1

    def update(self, mSec):
        if self.nrFrames > 1 and not self.paused:
            self.timeAccum += mSec / 1000.0
            #Loop through as many frames as is necessary
            while self.timeAccum > self.frameDuration:
                self.nextFrame()
                self.timeAccum -= self.frameDuration

    def draw(self, surface):
        if self.nrFrames > 1:
            surface.blit(self.gfx, tuple(self.pos), self.srcRect)
        else:
            surface.blit(self.gfx, tuple(self.pos))