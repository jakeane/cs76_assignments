# brew install pyqt
from IterativeAlphaBetaAI import IterativeAlphaBetaAI
from AlphaBetaAI import AlphaBetaAI
from PyQt5 import QtGui, QtSvg
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5.QtWidgets import QApplication, QWidget
import sys
import chess
import chess.svg
from RandomAI import RandomAI
from MinimaxAI import MinimaxAI
from ChessGame import ChessGame
from HumanPlayer import HumanPlayer

import random
from time import sleep


class ChessGui:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

        self.game = ChessGame(player1, player2)

        self.app = QApplication(sys.argv)
        self.svgWidget = QtSvg.QSvgWidget()
        self.svgWidget.setGeometry(50, 50, 400, 400)
        self.svgWidget.show()

    def start(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.make_move)
        self.timer.start(10)

        self.display_board()

    def display_board(self):
        svgboard = chess.svg.board(self.game.board)

        svgbytes = QByteArray()
        svgbytes.append(svgboard)
        self.svgWidget.load(svgbytes)

    def make_move(self):

        if not self.game.is_game_over():
            self.game.make_move()
            self.display_board()
        else:
            print("Game over!")
            sleep(10)
            self.game.make_move()


if __name__ == "__main__":

    random.seed(1)

    #player_ronda = RandomAI()

    # to do: gui does not work well with HumanPlayer, due to input() use on stdin conflict
    #   with event loop.

    player1 = IterativeAlphaBetaAI(True)  # RandomAI()
    player2 = AlphaBetaAI(3, False)

    game = ChessGame(player1, player2)
    gui = ChessGui(player1, player2)

    gui.start()

    sys.exit(gui.app.exec_())
