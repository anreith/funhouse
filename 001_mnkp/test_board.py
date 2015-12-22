#!/usr/bin/python3 -u

import random
import unittest
from board import Board

WIDTH    = 11
HEIGHT   = 13
ALLOWED  = ['a','b','c','d']
DISALLOWED = ['A','f','g','h',1,"string"]
CLEARVAL = None
NR_RANDOM_TESTS = 1000

class BoardTestCase(unittest.TestCase):
    def setUp(self):
        self.board = Board(WIDTH, HEIGHT, ALLOWED, CLEARVAL)
        random.seed()

    def testBoardInit(self):
        assert len(self.board.getData()) == WIDTH * HEIGHT
        assert not any(self.board.getData())

    def randomCoords(self):
        return (random.randint(0,WIDTH-1), random.randint(0,HEIGHT-1))

    def randomValue(self):
        return random.choice(ALLOWED)

    def testBoardBounds(self):
        for x in range(WIDTH):
            for y in range(HEIGHT):
                assert self.board.isWithinBounds(x,y)

        assert not self.board.isWithinBounds(-1,1)
        assert not self.board.isWithinBounds(1,-1)
        assert not self.board.isWithinBounds(WIDTH,0)
        assert not self.board.isWithinBounds(0,HEIGHT)
        
    def testBoardSetGet(self):
        for i in range(NR_RANDOM_TESTS):
            x,y = self.randomCoords()
            v = self.randomValue()
            self.board.set(x,y,v)
            assert self.board.get(x,y) == v

    def testIsAllowed(self):
        for a in ALLOWED:
            assert self.board.isAllowed(a)

        for a in DISALLOWED:
            assert not self.board.isAllowed(a)

    def testClear(self):
        assert self.board.isClear(5,5)
        self.board.set(5,5,ALLOWED[0])
        assert not self.board.isClear(5,5)
        self.board.clear(5,5)
        assert self.board.isClear(5,5)

        for x in range(WIDTH):
            for y in range(HEIGHT):
                self.board.set(x,y,ALLOWED[0])

        assert all(self.board.getData())
        self.board.clearAll()
        assert not any(self.board.getData())
        
if __name__ == "__main__":
    unittest.main()
