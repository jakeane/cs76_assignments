import random
import numpy as np
import math
import sys
from time import sleep


class HMMMaze:

    def __init__(self, maze_filename, colors):

        random.seed()
        self.read_maze(maze_filename)

        self.colors = colors

        self.pos_probs = np.array([[math.log(1 / (self.width * self.height))
                                    for _ in range(self.width)]
                                   for _ in range(self.height)])

        self.tran_model = np.array([[random.choice(colors)
                                     for _ in range(self.width)]
                                    for _ in range(self.height)])

        self.moves = [(1, 0), (0, 1), (-1, 0), (0, -1)]

        self.transitions = np.array([[self.num_neighbors((x, y))
                                      for x in range(self.width)]
                                     for y in range(self.height)])

    def read_maze(self, maze_filename):
        f = open(maze_filename)

        self.maze = np.array([[char if char == "#" else random.choice(colors)
                               for char in line
                               if char != "\n"]
                              for line in f])

        f.close()
        self.width = len(self.maze[0])
        self.height = len(self.maze)

    def num_neighbors(self, pos):
        neighbors = 0
        for move in self.moves:
            new_pos = tuple(map(sum, zip(pos, move)))
            if self.is_floor(new_pos):
                neighbors += 1
        return neighbors

    def generate_sequence(self, total_moves=10):
        random.seed()
        curr_pos = (random.choice(range(self.width)),
                    random.choice(range(self.height)))

        while not self.is_floor(curr_pos):
            curr_pos = (random.choice(range(self.width)),
                        random.choice(range(self.height)))

        seq = []
        pos_list = []

        for _ in range(total_moves):
            move = random.choice(self.moves)
            new_pos = tuple(map(sum, zip(curr_pos, move)))
            if self.is_floor(new_pos):
                curr_pos = new_pos
            seq.append(self.scan_color(curr_pos))
            pos_list.append(curr_pos)

        return seq, pos_list

    def scan_color(self, pos):
        true_color = self.maze[pos[1]][pos[0]]
        weights = [0.88 if true_color == color else 0.04
                   for color in self.colors]
        return random.choices(self.colors, weights=weights)[0]

    def determine_seq(self, seq, pos_list):
        curr_state = np.array([[self.floor_prob(seq[0], x, y)
                                for x in range(self.width)]
                               for y in range(self.height)])
        curr_state /= curr_state.sum()
        curr_state = np.ma.log(curr_state).filled(float('-inf'))
        self.print_time_step(
            curr_state, pos_list[0], seq[0], pos_list[:1])

        print("--------------------------------")

        for i, color in enumerate(seq[1:]):
            pos_prob = np.array([[self.floor_prob(color, x, y)
                                  for x in range(self.width)]
                                 for y in range(self.height)])

            pos_prob = np.ma.log(pos_prob).filled(float('-inf'))

            next_prob = [[float('-inf')
                          for x in range(self.width)]
                         for y in range(self.height)]

            for x in range(self.width):
                for y in range(self.height):
                    if self.is_floor((x, y)):
                        tran_model = self.generate_transition((x, y))

                        mult = np.array([[self.mult_tran(tran_model, curr_state, x, y)
                                          for x in range(self.width)]
                                         for y in range(self.height)])

                        next_prob[y][x] = np.log(mult.sum())
                    # for Viterbi, get max and it's index

            pos_prob += np.array(next_prob)

            curr_state = self.normalize_log(pos_prob)

            self.print_time_step(
                curr_state, pos_list[i+1], color, pos_list[:i+2])
            print("--------------------------------")

        return curr_state

    def floor_prob(self, color, x, y):
        return 0 if not self.is_floor((x, y)) \
            else 0.88 if self.maze[y][x] == color \
            else 0.04

    def is_floor(self, pos):
        if pos[0] < 0 or pos[0] >= self.width:
            return False
        if pos[1] < 0 or pos[1] >= self.height:
            return False

        return self.maze[pos[1]][pos[0]] != "#"

    def generate_transition(self, pos):

        prev_pos = {tuple(map(sum, zip(pos, move)))
                    for move in self.moves
                    if self.is_floor(tuple(map(sum, zip(pos, move))))}

        tran_model = np.array([[0.25 if (x, y) in prev_pos
                                else 1 - (0.25 * self.transitions[y][x]) if (x, y) == pos
                                else 0
                                for x in range(self.width)]
                               for y in range(self.height)])

        return np.array(tran_model)

    def mult_tran(self, tran_model, state_model, x, y):
        return tran_model[y][x] * math.exp(state_model[y][x])

    def convert_probs(self, final_state):
        linear_state = np.array([[math.exp(x) for x in row]
                                 for row in final_state])
        return np.round(linear_state * 100, 1)

    def normalize_log(self, curr_state):
        linear_state = np.array([[math.exp(x) for x in row]
                                 for row in curr_state])
        linear_state /= linear_state.sum()

        return np.ma.log(linear_state).filled(float('-inf'))

    def print_time_step(self, curr_state, curr_pos, curr_color, curr_path):
        maze_output = "Scanned: '{}' at {}\n".format(curr_color, curr_path[-1])
        maze_output += "Maze:\t\tProbabilities:\n"

        linear_state = self.convert_probs(curr_state)

        for i, row in enumerate(self.maze):
            if curr_pos[1] != i:
                maze_output += " " + " ".join(row) + " \t"
            else:
                maze_output += " "
                for j, col in enumerate(row):
                    if curr_pos[0] == j:
                        maze_output = maze_output[:-1]
                        maze_output += "(" + col + ")"
                    else:
                        maze_output += col + " "
                maze_output += "\t"

            for j, col in enumerate(linear_state[i]):
                if self.maze[i][j] == "#":
                    maze_output += "##" if j == 0 else " ##"
                else:
                    # "%02d" % col + str(col % 1)[1:3]
                    maze_output += " " + str(int(col)).zfill(2)

            maze_output += "\n\n"

        maze_output += "Current path: {}".format(curr_path)
        sleep(1)
        print(maze_output)


if __name__ == "__main__":

    colors = ["r", "g", "b", "y"]

    maze = HMMMaze(sys.argv[1], colors)

    seq, pos_list = maze.generate_sequence(sys.argv[2])
    final_state = maze.determine_seq(seq, pos_list)
