from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from random import randrange
import numpy as np

MS_SIZE = 8
CLOSE, OPEN, FLAG = 0, 1, 2


class Game:
    def __init__(self, number_of_mines=10):
        self.init_game_board()
        self.init_mine_map(number_of_mines)
        self.count_mines()

    def init_game_board(self):
        self.game_board = np.array(
            [[0 for i in range(MS_SIZE)] for j in range(MS_SIZE)])

    def init_mine_map(self, number_of_mines):
        self.mine_map = np.array([[0 for i in range(MS_SIZE)]
                                 for j in range(MS_SIZE)])

        if number_of_mines > MS_SIZE ** 2:
            number_of_mines = MS_SIZE ** 2

        a = [(i, j) for i in range(MS_SIZE) for j in range(MS_SIZE)]

        for i in range(len(a) - 1, 1, -1):
            j = randrange(i)
            tmp = a[i]
            a[i] = a[j]
            a[j] = tmp

        for i in range(number_of_mines):
            self.mine_map[a[i]] = -1

    def count_mines(self):
        tmp = np.array([[0 for i in range(MS_SIZE)] for j in range(MS_SIZE)])

        for i in range(MS_SIZE):
            for j in range(MS_SIZE):
                if self.mine_map[i][j] != -1:
                    tmp[i][j] = 0 - \
                        self.mine_map[max(i - 1, 0):i + 2,
                                      max(j - 1, 0):j + 2].sum()

        self.mine_map = self.mine_map + tmp

    def open_cell(self, x, y):
        if self.game_board[y][x] == 2:
            self.game_board[y][x] = 1
        if self.mine_map[y][x] == -1:
            return False
        elif self.game_board[y][x] != 1:
            for k in range(-1, 2):
                for l in range(-1, 2):
                    if y + k == -1 or y + k == MS_SIZE or x + l == -1 or x + l == MS_SIZE:
                        continue
                    elif self.mine_map[y + k][x + l] != -1 and self.game_board[y + k][x + l] != 2:
                        self.game_board[y + k][x + l] = 1

        return True

    def flag_cell(self, x, y):
        if self.game_board[y][x] == 2:
            self.game_board[y][x] = 0
        elif self.game_board[y][x] != 1:
            self.game_board[y][x] = 2

    def is_finished(self):
        if np.any((self.mine_map == -1) + (self.game_board == 1) - 1):
            return False
        return True
