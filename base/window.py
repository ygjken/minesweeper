from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from base.game import *


class MyPushButton(QPushButton):

    def __init__(self, text, x, y, parent):
        super(MyPushButton, self).__init__(text, parent)
        self.parent = parent
        self.x = x
        self.y = y
        self.setMinimumSize(25, 25)
        self.setSizePolicy(QSizePolicy.MinimumExpanding,
                           QSizePolicy.MinimumExpanding)

    def set_bg_color(self, colorname):
        self.setStyleSheet(
            "MyPushButton{{background-color: {}}}".format(colorname))

    def on_click(self):
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ShiftModifier:
            self.parent.game.flag_cell(self.x, self.y)
        else:
            if not self.parent.game.open_cell(self.x, self.y):
                self.parent.show_answer()
                QMessageBox.warning(self.parent, "Warning", "Game Over!")
                self.parent.close()

        self.parent.show_cell_status()
        if self.parent.game.is_finished():
            self.parent.show_cell_status()
            QMessageBox.warning(self.parent, "Warning", "Game Clear")
            self.parent.close()


class MinesweeperWindow(QMainWindow):

    def __init__(self):
        super(MinesweeperWindow, self).__init__()
        self.game = Game()
        self.initUI()
        self.show_cell_status()

    def initUI(self):
        self.resize(500, 500)
        self.setWindowTitle('Minesweeper')

        self.statusBar().showMessage("Shift + Click:  Set a flag")

        self.button = [[MyPushButton("x", x, y, self)
                        for x in range(MS_SIZE)] for y in range(MS_SIZE)]
        for y in range(MS_SIZE):
            for x in range(MS_SIZE):
                self.button[y][x].clicked.connect(self.button[y][x].on_click)

        vbox = QVBoxLayout()
        for j in range(MS_SIZE):
            hbox = QHBoxLayout()
            for i in range(MS_SIZE):
                hbox.addWidget(self.button[j][i])
            vbox.addLayout(hbox)

        container = QWidget()
        container.setLayout(vbox)
        self.setCentralWidget(container)
        self.show()

    def show_cell_status(self):
        for j in range(MS_SIZE):
            for i in range(MS_SIZE):
                if self.game.game_board[j][i] == 0:
                    self.button[j][i].setText("x")
                    self.button[j][i].set_bg_color("white")
                elif self.game.game_board[j][i] == 1:
                    self.button[j][i].set_bg_color("aqua")
                    if self.game.mine_map[j][i] > 0:
                        self.button[j][i].setText(
                            str(self.game.mine_map[j][i]))
                    else:
                        self.button[j][i].setText(" ")
                elif self.game.game_board[j][i] == 2:
                    self.button[j][i].setText("🚩")
                    self.button[j][i].set_bg_color("yellow")

    def show_answer(self):
        for j in range(MS_SIZE):
            for i in range(MS_SIZE):
                if self.game.mine_map[j][i] == -1:
                    self.button[j][i].setText("💣")
                    self.button[j][i].set_bg_color("red")
