import enum
import chess
import random
import numpy as np


class AlphaBetaAI():
    # need to init who the player is, white or black
    def __init__(self, depth, is_white):
        self.depth = depth
        self.is_white = is_white
        self.num_alphabeta = 0

    def choose_move(self, board):

        values = []
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        moves = list(board.legal_moves)
        random.shuffle(moves)
        for move in moves:
            board.push(move)
            new_val = self.min_value(board, self.depth, alpha, beta)
            values.append(new_val)
            best_value = max(best_value, new_val)
            alpha = max(alpha, new_val)
            board.pop()

        best_moves = [i for i, val in enumerate(values) if val == best_value]
        choice = random.choice(best_moves)
        return list(board.legal_moves)[choice]

    def max_value(self, board, depth, alpha, beta):
        self.num_alphabeta += 1
        if self.cutoff_test(board, depth):
            return self.simple_eval(board, False)

        value = float('-inf')

        moves = list(board.legal_moves)
        random.shuffle(moves)
        for move in moves:
            board.push(move)
            new_val = self.min_value(board, depth - 1, alpha, beta)
            value = max(value, new_val)
            alpha = max(alpha, new_val)
            if alpha >= beta:
                board.pop()
                return value
            board.pop()
        return value

    def min_value(self, board, depth, alpha, beta):
        self.num_alphabeta += 1
        if self.cutoff_test(board, depth):
            return self.simple_eval(board, True)

        value = float('inf')

        moves = list(board.legal_moves)
        random.shuffle(moves)
        for move in moves:
            board.push(move)
            new_val = self.max_value(board, depth - 1, alpha, beta)
            value = min(value, new_val)
            beta = min(beta, new_val)
            if alpha >= beta:
                board.pop()
                return value
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
        print(color+"AlphaBetaAI with cutoff depth "+str(self.depth) +
              " searched "+str(self.num_alphabeta)+" nodes")
