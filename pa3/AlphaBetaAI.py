from MinimaxAI import MinimaxAI
import enum
import chess
import random
import numpy as np


class AlphaBetaAI():
    def __init__(self, depth, is_white):
        self.depth = depth
        self.is_white = is_white
        self.num_alphabeta = 0

    def choose_move(self, board):
        # In order to check visits over duration of function
        start_num = self.num_alphabeta

        values = []
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        # randomize moves to allow variance
        moves = list(board.legal_moves)
        random.seed()
        random.shuffle(moves)

        for move in moves:
            board.push(move)

            # Get move value and add to list
            new_val = self.min_value(board, self.depth, alpha, beta)
            values.append(new_val)

            # Update if new max
            best_value = max(best_value, new_val)
            alpha = max(alpha, new_val)

            board.pop()

        # Print and return results
        print("After searching {} nodes, {} was selected by {} AlphaBeta.".format(
            self.num_alphabeta - start_num, moves[values.index(best_value)], "White" if self.is_white else "Black"))
        return moves[values.index(best_value)]

    def max_value(self, board, depth, alpha, beta):
        self.num_alphabeta += 1

        # Check if cutoff
        if self.cutoff_test(board, depth):
            return self.simple_eval(board)

        value = float('-inf')

        for move in list(board.legal_moves):
            board.push(move)

            # Get move value and update if new max
            value = max(value, self.min_value(board, depth - 1, alpha, beta))

            # Check if we can prune
            if value >= beta:
                board.pop()
                return value

            # Update alpha if new max
            alpha = max(alpha, value)

            board.pop()

        return value

    def min_value(self, board, depth, alpha, beta):
        self.num_alphabeta += 1

        # Check if cutoff
        if self.cutoff_test(board, depth):
            return self.simple_eval(board)

        value = float('inf')

        for move in list(board.legal_moves):
            board.push(move)

            # Get move value and update if new min
            value = min(value, self.max_value(board, depth - 1, alpha, beta))

            # Check if we can prune
            if alpha >= value:
                board.pop()
                return value

            # Update beta if new min
            beta = min(beta, value)

            board.pop()

        return value

    def cutoff_test(self, board, depth):
        return depth == 0 or board.is_game_over()

    def simple_eval(self, board):
        evaluation = 0

        # Check end game conditions
        if board.is_game_over():
            if board.is_stalemate():
                return evaluation
            if board.is_checkmate():
                if board.turn != self.is_white:
                    evaluation += 300
                else:
                    evaluation -= 300

        # Tally difference in pieces between each side
        board_status = [len(board.pieces(i, True)) -
                        len(board.pieces(i, False)) for i in range(1, 7)]

        # Account if player is black or white
        player_coef = 1 if self.is_white else -1

        # Multiply each tally by respective material value. Then sum
        return evaluation + player_coef * sum(np.multiply(board_status, [1, 3, 3, 5, 9, 200]))

    def end_report(self):
        color = "White " if self.is_white else "Black "
        print(color+"AlphaBetaAI with cutoff depth "+str(self.depth) +
              " searched "+str(self.num_alphabeta)+" nodes")
