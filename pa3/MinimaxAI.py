import enum
import chess
import random
import numpy as np
import time


class MinimaxAI():
    # need to init who the player is, white or black
    def __init__(self, depth, is_white, use_book=False):
        self.depth = depth
        self.is_white = is_white
        self.num_minimax = 0
        self.time = 0
        self.use_book = use_book

    def choose_move(self, board):

        start_num = self.num_minimax
        start_time = time.time()

        # Use opening book if option set
        if self.use_book:
            with chess.polyglot.open_reader("data/performance.bin") as reader:
                try:
                    entry = reader.weighted_choice(board)
                    time.sleep(1)

                    print("After considering {} options from the entry book, {} was selected by {} MinimaxAI.".format(
                        sum(1 for _ in reader.find_all(board)), entry.move, "White" if self.is_white else "Black"))
                    self.time += time.time() - start_time
                    reader.close()

                    return entry.move

                except IndexError:
                    reader.close()

        # init
        values = []

        # Randomize moves to allow variance
        moves = list(board.legal_moves)
        random.seed()
        random.shuffle(moves)

        for move in moves:
            board.push(move)
            values.append(self.min_value(board, self.depth))
            board.pop()

        # Print and return results
        print("After searching {} nodes, {} was selected by {} MinimaxAI.".format(
            self.num_minimax - start_num, moves[values.index(max(values))], "White" if self.is_white else "Black"))
        self.time += time.time() - start_time
        return moves[values.index(max(values))]

    def max_value(self, board, depth):
        self.num_minimax += 1

        # Check if cutoff
        if self.cutoff_test(board, depth):
            return self.simple_eval(board, depth)

        value = float('-inf')
        for move in list(board.legal_moves):
            board.push(move)
            value = max(value, self.min_value(board, depth - 1))
            board.pop()
        return value

    def min_value(self, board, depth):
        self.num_minimax += 1

        # Check if cutoff
        if self.cutoff_test(board, depth):
            return self.simple_eval(board, depth)

        value = float('inf')
        for move in list(board.legal_moves):
            board.push(move)
            value = min(value, self.max_value(board, depth - 1))
            board.pop()
        return value

    def cutoff_test(self, board, depth):
        return depth == 0 or board.is_game_over()

    def simple_eval(self, board, depth):
        evaluation = 0

        # Check end game conditions
        if board.is_game_over():
            if board.is_stalemate():
                return evaluation
            if board.is_checkmate():
                if board.turn != self.is_white:
                    evaluation += 200 + (50 * depth)
                else:
                    evaluation -= 200 + (50 * depth)

        # Tally difference in pieces between each side
        board_status = [len(board.pieces(i, True)) -
                        len(board.pieces(i, False)) for i in range(1, 7)]

        # Account if player is black or white
        player_coef = 1 if self.is_white else -1

        # Multiply each tally by respective material value. Then sum
        return evaluation + player_coef * sum(np.multiply(board_status, [1, 3, 3, 5, 9, 200]))

    def end_report(self):
        color = "White" if self.is_white else "Black"
        print("{} MinimaxAI with cutoff depth {} searched {} nodes and spent {} seconds".format(
            color, self.depth, self.num_minimax, int(self.time)))
