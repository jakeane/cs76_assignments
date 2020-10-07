from AlphaBetaAI import AlphaBetaAI
import enum
import chess
import random
import numpy as np


class MinimaxAI():
    # need to init who the player is, white or black
    def __init__(self, depth, is_white):
        self.depth = depth
        self.is_white = is_white
        self.num_minimax = 0
        self.alphabetaAI = AlphaBetaAI(self.depth, self.is_white)

    def choose_move(self, board):

        values = []

        for move in list(board.legal_moves):
            board.push(move)
            values.append(self.min_value(board, self.depth))
            board.pop()

        # print("moves: " + str(list(board.legal_moves)))
        # print("results: " + str(values))
        best_value = max(values)

        if self.alphabetaAI.choose_move(board) != best_value:
            print("RED ALERT")
        best_moves = [i for i, val in enumerate(values) if val == best_value]
        choice = random.choice(best_moves)
        # print("choice: " + str(list(board.legal_moves)[choice]))
        return list(board.legal_moves)[choice]

    def max_value(self, board, depth):
        self.num_minimax += 1
        if self.cutoff_test(board, depth):
            return self.simple_eval(board, False)

        value = float('-inf')
        for move in list(board.legal_moves):
            board.push(move)
            value = max(value, self.min_value(board, depth - 1))
            board.pop()
        return value

    def min_value(self, board, depth):
        self.num_minimax += 1
        if self.cutoff_test(board, depth):
            return self.simple_eval(board, True)

        value = float('inf')
        for move in list(board.legal_moves):
            board.push(move)
            value = min(value, self.max_value(board, depth - 1))
            board.pop()
        return value

    def cutoff_test(self, board, depth):
        return depth == 0 or board.is_game_over()

    def simple_eval(self, board, side):
        if board.is_game_over():
            if board.is_stalemate():
                return 0
            if board.is_checkmate():
                if side:
                    return 300
                else:
                    return -300

        board_status = [len(board.pieces(i, True)) -
                        len(board.pieces(i, False)) for i in range(1, 7)]

        player_coef = 1 if self.is_white else -1
        return player_coef * sum(np.multiply(board_status, [1, 3, 3, 5, 9, 200]))

    def end_report(self):
        color = "White " if self.is_white else "Black "
        print(color+"MinimaxAI with cutoff depth "+str(self.depth) +
              " searched "+str(self.num_minimax)+" nodes")
