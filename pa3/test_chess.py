# pip3 install python-chess


import chess
from RandomAI import RandomAI
from HumanPlayer import HumanPlayer
from MinimaxAI import MinimaxAI
from AlphaBetaAI import AlphaBetaAI
from ChessGame import ChessGame


import sys
import numpy as np


player1 = AlphaBetaAI(3, True)  # HumanPlayer()
player2 = AlphaBetaAI(3, False)  # RandomAI()

game: ChessGame = ChessGame(player1, player2)


while not game.is_game_over():
    print(game)
    game.make_move()
print(game)

player1.end_report()
player2.end_report()
# print(hash(str(game.board)))
