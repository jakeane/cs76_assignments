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
            print("The winner is {}".format(
                "Black" if self.game.board.turn else "White"))
            game.players[0].end_report()
            game.players[1].end_report()
            sleep(100)


if __name__ == "__main__":

    random.seed()

    #player_ronda = RandomAI()

    # to do: gui does not work well with HumanPlayer, due to input() use on stdin conflict
    #   with event loop.

    player1 = AlphaBetaAI(4, True)  # RandomAI()
    player2 = AlphaBetaAI(4, False)

    game = ChessGame(player1, player2)
    gui = ChessGui(player1, player2)

    gui.start()

    sys.exit(gui.app.exec_())

# [Move.from_uci('a2a3'), Move.from_uci('g2g3'), Move.from_uci('c2c4'), Move.from_uci('a2a4'), Move.from_uci('c2c3'), Move.from_uci('g1h3'), Move.from_uci('d2d4'), Move.from_uci('g1f3'),
# Move.from_uci('e2e4'), Move.from_uci('f2f3'), Move.from_uci('b2b3'), Move.from_uci('g2g4'), Move.from_uci('f2f4'), Move.from_uci('h2h4'), Move.from_uci('e2e3'), Move.from_uci('b1a3'),
# Move.from_uci('d2d3'), Move.from_uci('b1c3'), Move.from_uci('b2b4'), Move.from_uci('h2h3')]
