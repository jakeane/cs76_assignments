import random
import numpy as np
import time


class IterativeAlphaBetaAI():
    # need to init who the player is, white or black
    def __init__(self, is_white, time_limit=3):
        self.is_white = is_white
        self.time_limit = time_limit
        self.num_alphabeta = 0
        self.start = time.time()
        self.moves = 0
        self.total_depth = 0

    def choose_move(self, board):

        self.moves += 1

        moves = list(board.legal_moves)
        random.seed()
        random.shuffle(moves)

        best_move = moves[0]
        self.start = time.time()

        for i in range(1, 10):
            values = []
            best_value = float('-inf')
            alpha = float('-inf')
            beta = float('inf')

            for move in moves:
                board.push(move)
                new_val = self.min_value(board, i, alpha, beta)
                values.append(new_val)
                best_value = max(best_value, new_val)
                alpha = max(alpha, new_val)
                board.pop()
            if time.time() - self.start > self.time_limit:
                print(time.time() - self.start)
                print("---------------------------------")
                self.total_depth += i - 1
                return best_move
            best_move = moves[values.index(best_value)]
            print("At depth {}, the best move is {}".format(i, best_move))
        print("---------------------------------")
        return best_move

    def max_value(self, board, depth, alpha, beta):
        self.num_alphabeta += 1
        if self.cutoff_test(board, depth):
            return self.simple_eval(board, depth)

        value = float('-inf')

        moves = list(board.legal_moves)
        moves.sort(key=lambda move: self.move_comparator(
            board, move, depth), reverse=True)

        for move in moves:
            board.push(move)

            value = max(value, self.min_value(
                board, depth - 1, alpha, beta))

            if value >= beta or time.time() - self.start > self.time_limit:
                board.pop()
                return value
            alpha = max(alpha, value)
            board.pop()
        return value

    def min_value(self, board, depth, alpha, beta):
        self.num_alphabeta += 1
        if self.cutoff_test(board, depth):
            return self.simple_eval(board, depth)

        value = float('inf')

        moves = list(board.legal_moves)
        moves.sort(key=lambda move: self.move_comparator(board, move, depth))

        for move in moves:
            board.push(move)

            value = min(value, self.max_value(
                board, depth - 1, alpha, beta))

            if alpha >= value or time.time() - self.start > self.time_limit:
                board.pop()
                return value
            beta = min(beta, value)
            board.pop()
        return value

    def move_comparator(self, board, move, depth):
        board.push(move)
        value = self.simple_eval(board, depth)
        board.pop()
        return value

    def cutoff_test(self, board, depth):
        return depth == 0 or board.is_game_over()

    def simple_eval(self, board, depth):
        evaluation = 0

        if board.is_game_over():
            if board.is_stalemate():
                return evaluation
            if board.is_checkmate():
                if board.turn != self.is_white:
                    evaluation += 200 + (50 * depth)
                else:
                    evaluation -= 200 + (50 * depth)

        board_status = [len(board.pieces(i, True)) -
                        len(board.pieces(i, False)) for i in range(1, 7)]

        player_coef = 1 if self.is_white else -1
        return evaluation + player_coef * sum(np.multiply(board_status, [1, 3, 3, 5, 9, 200]))

    def end_report(self):
        color = "White " if self.is_white else "Black "
        print("{} IterativeAlphaBetaAI searched {} nodes averaging a depth of {}".format(
            color, self.num_alphabeta, self.total_depth / self.moves))
