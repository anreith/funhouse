#!/usr/bin/python3 -u

import sys
sys.path.insert(1, "../lib")

from itertools import chain, cycle
from board import Board, in_a_row
from keyboard import get_tuple_int
import argparse

CLEARVAL = ' '

__doc__ = '''This program lets p number of players play an m,n,k game.
             See: https://en.wikipedia.org/wiki/M,n,k-game .
             Default is 2 player 3,3,3 (tic-tac-toe)
          '''

def play(width, height, inarow, players):
    gameboard = Board(width, height, players, clearval=' ')
    turns = cycle(players)

    while True:
        player = next(turns)
        print("'{}' turn. Choose coordinates 'x,y':".format(player))
        x,y = get_tuple_int(0, 0, width, height)
        while not gameboard.isClear(x,y):
            print("Square is taken, please choose free coordinates 'x,y':")
            x,y = get_tuple_int(0, 0, width, height)

        gameboard.set(x,y,player)
        gameboard.print()

        if in_a_row(gameboard, inarow):
            print("Winner is: {}".format(player))
            break;

        if gameboard.filled():
            print("Draw")
            break;

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', type=int, help="game board width",  default=3)
    parser.add_argument('-n', type=int, help="game board height", default=3)
    parser.add_argument('-k', type=int, help="required in a row to win" , default=3)
    parser.add_argument('-p', type=str, help="players as characters in string", default="xo")
    args = parser.parse_args()

    assert CLEARVAL not in args.p, "incorrect player argument"
    assert args.k >= args.m or args.k >= args.n, "Invalid game board dimensions for given k"

    print("m:{} n:{} k:{} p:{}".format(args.m, args.n, args.k, len(args.p)))
    play(args.m, args.n, args.k, args.p)
