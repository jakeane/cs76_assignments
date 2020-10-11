import random
import numpy as np
import time
from chess.polyglot import zobrist_hash, open_reader


class TranspoIterativeAlphaBetaAI():
    # need to init who the player is, white or black
    def __init__(self, is_white, time_limit=3, use_book=False):
        self.is_white = is_white
        self.time_limit = time_limit
        self.num_alphabeta = 0
        self.start = time.time()
        self.moves = 0
        self.total_depth = 0
        self.use_book = use_book
        self.transposition_max = dict()
        self.transposition_min = dict()

    def choose_move(self, board):

        # Query opening book if option set
        if self.use_book:
            with open_reader("data/performance.bin") as reader:
                try:
                    entry = reader.weighted_choice(board)
                    time.sleep(1)

                    print("After considering {} options from the entry book, {} was selected by {} MinimaxAI.".format(
                        sum(1 for _ in reader.find_all(board)), entry.move, "White" if self.is_white else "Black"))
                    reader.close()

                    return entry.move

                except IndexError:
                    reader.close()

        self.moves += 1

        moves = list(board.legal_moves)
        random.seed()
        random.shuffle(moves)

        # init
        best_move = moves[0]
        self.start = time.time()
        self.transposition_max.clear()
        self.transposition_min.clear()
        print("---------------------------------")

        # iterate through depths, likely will not be surpassed
        for i in range(1, 20):

            # iteration init
            values = []
            best_value = float('-inf')
            alpha = float('-inf')
            beta = float('inf')

            for move in moves:
                board.push(move)

                # Get move value and add to list
                new_val = self.min_value(board, i, alpha, beta)
                values.append(new_val)

                # Update if new max
                best_value = max(best_value, new_val)
                alpha = max(alpha, new_val)

                board.pop()

            # If time limit reached, return
            if time.time() - self.start > self.time_limit:
                print("---------------------------------")
                self.total_depth += i - 1
                return best_move

            # If not reached, update best move
            best_move = moves[values.index(best_value)]
            print("At depth {}, the best move is {}".format(i, best_move))

        print("---------------------------------")
        return best_move

    def max_value(self, board, depth, alpha, beta):
        self.num_alphabeta += 1

        # Check if cutoff
        if self.cutoff_test(board, depth):
            return self.simple_eval(board, depth, True)

        value = float('-inf')

        moves = list(board.legal_moves)
        moves.sort(key=lambda move: self.move_comparator(
            board, move, depth, True), reverse=True)

        for move in moves:
            board.push(move)

            if zobrist_hash(board) in self.transposition_max:
                board_depths = self.transposition_max[zobrist_hash(board)]

                # If value was found at current or earlier depth
                # Use that as value, otherwise, find and assign
                max_depth = max(board_depths)
                if max_depth > depth and (max_depth - depth) % 2 == 0:
                    new_value = board_depths[max_depth]
                elif depth in board_depths:
                    new_value = board_depths[depth]
                else:
                    new_value = self.min_value(board, depth - 1, alpha, beta)
                    board_depths[depth] = new_value
            # If state not found, find and assign
            else:
                new_value = self.min_value(board, depth - 1, alpha, beta)
                self.transposition_max[zobrist_hash(board)] = {
                    depth: new_value
                }

            value = max(value, new_value)

            # Check if we can prune or time limit reached
            if value >= beta or time.time() - self.start > self.time_limit:
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
            return self.simple_eval(board, depth, False)

        value = float('inf')

        moves = list(board.legal_moves)
        moves.sort(key=lambda move: self.move_comparator(
            board, move, depth, False))

        for move in moves:
            board.push(move)

            if zobrist_hash(board) in self.transposition_min:
                board_depths = self.transposition_min[zobrist_hash(board)]

                # If value was found at current or earlier depth
                # Use that as value, otherwise, find and assign
                max_depth = max(board_depths)
                if max_depth > depth and (max_depth - depth) % 2 == 0:
                    new_value = board_depths[max_depth]
                elif depth in board_depths:
                    new_value = board_depths[depth]
                else:
                    new_value = self.min_value(board, depth - 1, alpha, beta)
                    board_depths[depth] = new_value
            # If state not found, find and assign
            else:
                new_value = self.min_value(board, depth - 1, alpha, beta)
                self.transposition_min[zobrist_hash(board)] = {
                    depth: new_value
                }

            value = min(value, new_value)

            # Check if we can prune or time limit has been reached
            if alpha >= value or time.time() - self.start > self.time_limit:
                board.pop()
                return value

            # Update beta if new min
            beta = min(beta, value)

            board.pop()

        return value

    def move_comparator(self, board, move, depth, side):
        board.push(move)

        transposition_table = self.transposition_max if side else self.transposition_min

        if zobrist_hash(board) in transposition_table:
            board_depths = transposition_table[zobrist_hash(board)]

            # If value was found at current or earlier depth
            # Use that as value, otherwise, find and assign
            max_depth = max(board_depths)
            if max_depth > depth and (max_depth - depth) % 2 == 0:
                value = board_depths[max_depth]
            elif depth in board_depths:
                value = board_depths[depth]
            else:
                value = self.simple_eval(board, depth, side)
        # If state not found, find and assign
        else:
            value = self.simple_eval(board, depth, side)

        board.pop()
        return value

    def cutoff_test(self, board, depth):
        return depth == 0 or board.is_game_over()

    def simple_eval(self, board, depth, side):

        # If the board is in the transposition table,
        # then a more accurate evaluation is possible
        transposition_table = self.transposition_max if side else self.transposition_min
        if zobrist_hash(board) in transposition_table:
            board_depths = transposition_table[zobrist_hash(board)]

            max_depth = max(board_depths)
            if (max_depth - depth) % 2 == 0:
                return board_depths[max_depth]

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
        print("{} IterativeAlphaBetaAI searched {} nodes averaging a depth of {}".format(
            color, self.num_alphabeta, self.total_depth / self.moves))
