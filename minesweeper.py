import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from base.game import *
from base.window import *

MS_SIZE = 8
CLOSE, OPEN, FLAG = 0, 1, 2


def main():
    app = QApplication(sys.argv)
    w = MinesweeperWindow()
    app.exec_()


if __name__ == '__main__':
    main()
