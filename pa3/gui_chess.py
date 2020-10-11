# brew install pyqt
from NullAlphaBetaAI import NullAlphaBetaAI
from SortAlphaBetaAI import SortAlphaBetaAI
from IterativeAlphaBetaAI import IterativeAlphaBetaAI
from AlphaBetaAI import AlphaBetaAI
from NonOptAlphaBetaAI import NonOptAlphaBetaAI
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
            if self.game.board.is_checkmate():
                print("The winner is {}".format(
                    "Black" if self.game.board.turn else "White"))
            else:
                print("The game resulted in a tie!")
            game.players[0].end_report()
            game.players[1].end_report()
            sleep(100)


if __name__ == "__main__":

    random.seed(1300)

    #player_ronda = RandomAI()

    # to do: gui does not work well with HumanPlayer, due to input() use on stdin conflict
    #   with event loop.

    player1 = IterativeAlphaBetaAI(True, 5, True)  # AlphaBetaAI(4, True)
    player2 = SortAlphaBetaAI(2, False, True)

    game = ChessGame(player1, player2)
    gui = ChessGui(player1, player2)

    gui.start()

    sys.exit(gui.app.exec_())
