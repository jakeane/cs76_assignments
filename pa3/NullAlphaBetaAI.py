import random
import numpy as np
import time
import chess


class NullAlphaBetaAI():
    def __init__(self, depth, is_white, use_book=False):
        self.depth = depth
        self.is_white = is_white
        self.num_alphabeta = 0
        self.time = 0
        self.use_book = use_book

    def choose_move(self, board):
        # In order to check visits over duration of function
        start_num = self.num_alphabeta
        start_time = time.time()

        # Query opening book if option set
        if self.use_book:
            with chess.polyglot.open_reader("data/performance.bin") as reader:
                try:
                    entry = reader.weighted_choice(board)
                    time.sleep(1)

                    print("After considering {} options from the entry book, {} was selected by {} NullAlphaBetaAI.".format(
                        sum(1 for _ in reader.find_all(board)), entry.move, "White" if self.is_white else "Black"))
                    self.time += time.time() - start_time
                    reader.close()

                    return entry.move

                except IndexError:
                    reader.close()

        # init
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
        print("After searching {} nodes, {} was selected by {} NullAlphaBetaAI.".format(
            self.num_alphabeta - start_num, moves[values.index(best_value)], "White" if self.is_white else "Black"))
        self.time += time.time() - start_time
        return moves[values.index(best_value)]

    def max_value(self, board, depth, alpha, beta):
        self.num_alphabeta += 1

        # Check if cutoff
        if self.cutoff_test(board, depth):
            return self.simple_eval(board, depth)

        # Null move pruning
        if not board.is_check():
            board.push(chess.Move.null())
            null_val = -self.min_value(board, depth -
                                       2, -beta, -beta + 1)
            board.pop()
            if null_val >= beta:
                return beta

        value = float('-inf')

        moves = list(board.legal_moves)
        moves.sort(key=lambda move: self.move_comparator(
            board, move, depth), reverse=True)

        for move in moves:
            board.push(move)

            new_value = self.min_value(board, depth - 1, alpha, beta)

            value = max(value, new_value)

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
            return self.simple_eval(board, depth)

        value = float('inf')

        moves = list(board.legal_moves)
        moves.sort(key=lambda move: self.move_comparator(board, move, depth))

        for move in moves:
            board.push(move)

            new_value = self.max_value(board, depth - 1, alpha, beta)
            value = min(value, new_value)

            # Check if we can prune
            if alpha >= value:
                board.pop()
                return value

            # Update beta if new min
            beta = min(beta, value)

            board.pop()

        return value

    def move_comparator(self, board, move, depth):
        value = 0
        board.push(move)
        value = self.simple_eval(board, depth)
        board.pop()
        return value

    def cutoff_test(self, board, depth):
        return depth <= 0 or board.is_game_over()

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
        print("{} NullAlphaBetaAI with cutoff depth {} searched {} nodes and spent {} seconds".format(
            color, self.depth, self.num_alphabeta, int(self.time)))
