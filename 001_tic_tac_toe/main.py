#!/usr/bin/python3 -u

from itertools import chain

board = [[None,None,None],
         [None,None,None],
         [None,None,None]]

def printboard():
    for y in board:
        for x in y:
            print(x or '_', end="")
        print("")

def free(x,y):
    return board[y][x] == None

def getcoords(minx, miny, maxx, maxy):
    x,y = tuple(int(x.strip()) for x in input().split(','))
    while x < minx or x > maxx or y < miny or y > maxy:
        print("Coordinates out of bounds ({},{})-({},{}), insert again:".format(minx, miny, maxx, maxy))
        x,y = tuple(int(x.strip()) for x in input().split(','))

    return x,y

def checkDraw():
    return all(chain.from_iterable(board))

def checkWinner():
    for y in board:
        if y == ['x','x','x'] or y == ['o','o','o']:
            return True

    #Rotated, ie check vertical
    for y in zip(*board[::-1]):
        if y == ['x','x','x'] or y == ['o','o','o']:
            return True

    if board[0][0] and board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        return True

    if board[2][0] and board[2][0] == board[1][1] and board[1][1] == board[0][2]:
        return True

    return False

def round(current):
    printboard()
    print("'{}' turn. Choose coordinates (0,0)-(2,2):".format(current))
    minx, miny, maxx, maxy = 0, 0, 2, 2
    x,y = getcoords(minx, miny, maxx, maxy)
    while not free(x,y):
        print("Square is taken, please choose free coordinates:")
        printboard()
        x,y = getcoords(minx, miny, maxx, maxy)

    board[y][x] = current

def main():
  current = 'o'
  gameover = False
  while not gameover:
    current = 'x' if current == 'o' else 'o'
    round(current)
    gameover = checkWinner() or checkDraw()

  printboard()
  if checkWinner():
     print("Winner is: {}".format(current))
  else:
     print("Draw")

if __name__ == "__main__":
    main()
