#!/usr/bin/python3 -u

from itertools import chain, groupby, cycle
from board import Board

def printboard(gameboard):
    for row in gameboard.getRows():
        print("".join(row))

def getcoords(minx, miny, maxx, maxy):
    x,y = tuple(int(x.strip()) for x in input().split(','))
    while x < minx or x > maxx or y < miny or y > maxy:
        print("Coordinates out of bounds ({},{})-({},{}), insert again:".format(minx, miny, maxx, maxy))
        x,y = tuple(int(x.strip()) for x in input().split(','))

    return x,y

def checkWinner(gameboard, inarow, clearval):
    for row in gameboard.getRows():
        if next((v for v,n in groupby(row) if v != clearval and len(list(n)) >= inarow), None):
            return True

    for col in gameboard.getColumns():
        if next((v for v,n in groupby(col) if v != clearval and len(list(n)) >= inarow), None):
            return True

    return False

def round(current, gameboard):
    printboard(gameboard)
    print("'{}' turn. Choose coordinates 'x,y':".format(current))
    minx, miny, maxx, maxy = 0, 0, gameboard.getWidth(), gameboard.getHeight()
    x,y = getcoords(minx, miny, maxx, maxy)
    while not gameboard.isClear(x,y):
        print("Square is taken, please choose free coordinates 'x,y':")
        printboard(gameboard)
        x,y = getcoords(minx, miny, maxx, maxy)

    gameboard.set(x,y,current)

def main():
  players = "xo"
  turns = cycle(players)
  gameboard = Board(3, 3, players, clearval=' ')

  while True:
      player = next(turns)
      round(player, gameboard)

      if checkWinner(gameboard, 3, clearval=' '):
          print("Winner is: {}".format(player))
          break;

      if gameboard.filled():
          print("Draw")
          break;

if __name__ == "__main__":
    main()
