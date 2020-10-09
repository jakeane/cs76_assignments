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

    def choose_move(self, board):

        start_num = self.num_minimax

        moves = list(board.legal_moves)
        random.seed()
        random.shuffle(moves)

        values = []

        for move in moves:
            board.push(move)
            values.append(self.min_value(board, self.depth))
            board.pop()
        # return values
        print("After searching {} nodes, {} was selected by {} Minimax.".format(
            self.num_minimax - start_num, moves[values.index(max(values))], "White" if self.is_white else "Black"))
        return moves[values.index(max(values))]

    def max_value(self, board, depth):
        self.num_minimax += 1
        if self.cutoff_test(board, depth):
            return self.simple_eval(board)

        value = float('-inf')
        for move in list(board.legal_moves):
            board.push(move)
            value = max(value, self.min_value(board, depth - 1))
            board.pop()
        return value

    def min_value(self, board, depth):
        self.num_minimax += 1
        if self.cutoff_test(board, depth):
            return self.simple_eval(board)

        value = float('inf')
        for move in list(board.legal_moves):
            board.push(move)
            value = min(value, self.max_value(board, depth - 1))
            board.pop()
        return value

    def cutoff_test(self, board, depth):
        return depth == 0 or board.is_game_over()

    def simple_eval(self, board):
        evaluation = 0

        if board.is_game_over():
            if board.is_stalemate():
                return evaluation
            if board.is_checkmate():
                if board.turn != self.is_white:
                    evaluation += 300
                else:
                    evaluation -= 300

        board_status = [len(board.pieces(i, True)) -
                        len(board.pieces(i, False)) for i in range(1, 7)]

        player_coef = 1 if self.is_white else -1
        return evaluation + player_coef * sum(np.multiply(board_status, [1, 3, 3, 5, 9, 200]))

    def end_report(self):
        color = "White " if self.is_white else "Black "
        print(color+"MinimaxAI with cutoff depth "+str(self.depth) +
              " searched "+str(self.num_minimax)+" nodes")
