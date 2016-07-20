'''
Created on Apr 10, 2014

@author: anreith
'''

import os
import sys

import tower

class SuncatcherTower(tower.Tower):

    def __init__(self, data):
        tower.Tower.__init__(self, data)
        self.einterval = data["energyinterval"]
        self.espeed = data["energyspeed"]

    def clone(self):
        return SuncatcherTower(self.data)

    def update(self, mSec):
        tower.Tower.update(self, mSec)

        if self.timeAccum >= self.einterval:
            self.addEnergy(self, 3, self.espeed)
            self.timeAccum %= self.einterval