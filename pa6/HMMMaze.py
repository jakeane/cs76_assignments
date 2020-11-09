import random
import numpy as np
import math
import sys
from time import sleep


class HMMMaze:

    def __init__(self, maze_filename, colors, tpr=0.88):

        random.seed()
        self.read_maze(maze_filename)

        self.colors = colors

        self.moves = [(1, 0), (0, 1), (-1, 0), (0, -1)]

        # Get's number of neighbors for a given tile
        # Can be used to infer chance of hitting wall
        self.transitions = np.array([[self.num_neighbors((x, y))
                                      for x in range(self.width)]
                                     for y in range(self.height)])

        # Probability of accurate/inaccurate reading
        self.tpr = tpr
        self.fpr = (1 - tpr) / (len(self.colors) - 1)

    # Convert maze file into 2d array of walls/colors
    def read_maze(self, maze_filename):
        f = open(maze_filename)

        self.maze = np.array([[char if char == "#" else random.choice(colors)
                               for char in line
                               if char != "\n"]
                              for line in f])

        f.close()
        self.width = len(self.maze[0])
        self.height = len(self.maze)

    # Get num neighbors at given tile
    def num_neighbors(self, pos):
        neighbors = 0
        if self.is_floor(pos):
            for move in self.moves:
                new_pos = tuple(map(sum, zip(pos, move)))
                if self.is_floor(new_pos):
                    neighbors += 1
        return neighbors

    # Generate a sequence of movements and sensor readings
    def generate_sequence(self, total_moves=10):
        random.seed()
        curr_pos = (random.choice(range(self.width)),
                    random.choice(range(self.height)))

        # Yes, this is janky, but it ensures a wall cannot be selected
        while not self.is_floor(curr_pos):
            curr_pos = (random.choice(range(self.width)),
                        random.choice(range(self.height)))

        seq = []
        pos_list = []

        for _ in range(total_moves):
            # Determine movement
            move = random.choice(self.moves)
            new_pos = tuple(map(sum, zip(curr_pos, move)))
            if self.is_floor(new_pos):
                curr_pos = new_pos

            # Add to sequences
            seq.append(self.scan_color(curr_pos))
            pos_list.append(curr_pos)

        return seq, pos_list

    # Scan modeled by weighted choice
    def scan_color(self, pos):
        true_color = self.maze[pos[1]][pos[0]]
        weights = [self.tpr if true_color == color else self.fpr
                   for color in self.colors]
        return random.choices(self.colors, weights=weights)[0]

    # filtering algorithm
    def determine_seq(self, seq, pos_list):
        # Initial probability
        curr_state = np.array([[self.floor_prob(seq[0], x, y)
                                for x in range(self.width)]
                               for y in range(self.height)])
        curr_state /= curr_state.sum()

        # np.ma.log() can handle 0's in an array
        # they just need to be filled
        curr_state = np.ma.log(curr_state).filled(float('-inf'))

        self.print_time_step(
            curr_state, pos_list[0], seq[:1], pos_list[:1])
        print("--------------------------------")

        for i, color in enumerate(seq[1:]):
            # Get probability of evidence for each position
            # pos_prob = P(e_i|X_i)
            pos_prob = np.array([[self.floor_prob(color, x, y)
                                  for x in range(self.width)]
                                 for y in range(self.height)])

            pos_prob = np.ma.log(pos_prob).filled(float('-inf'))

            # init array to fill
            # next_prob = \sum_{x_i-1} P(X_i | x_{i-1}) * P(x_{i-1} | e_{0:i})
            next_prob = [[float('-inf')
                          for _ in range(self.width)]
                         for _ in range(self.height)]

            for x in range(self.width):
                for y in range(self.height):
                    if self.is_floor((x, y)):
                        # tran_model = P(X_i | x_{i-1})
                        tran_model = self.generate_transition((x, y))

                        # curr_state = P(x_{i-1} | e_{0:i})
                        # mult multiplies the two arrays
                        mult = np.array([[tran_model[y][x] * math.exp(curr_state[y][x])
                                          for x in range(self.width)]
                                         for y in range(self.height)])

                        # summation of x_{i-1}'s for X_i
                        next_prob[y][x] = np.log(mult.sum())

            # multiply probabilities
            pos_prob += np.array(next_prob)

            curr_state = self.normalize_log(pos_prob)

            self.print_time_step(
                curr_state, pos_list[i+1], seq[:i+2], pos_list[:i+2])
            print("--------------------------------")

        # Guess position based on probabilities
        top_prob = np.argmax(curr_state)
        end_pos = (top_prob % self.width,
                   top_prob // self.width)

        return end_pos

    # viterbi algorithm
    def determine_path(self, seq, pos_list):
        # Initial probability
        curr_state = np.array([[self.floor_prob(seq[0], x, y)
                                for x in range(self.width)]
                               for y in range(self.height)])
        curr_state /= curr_state.sum()

        # np.ma.log() can handle 0's in an array
        # they just need to be filled
        curr_state = np.ma.log(curr_state).filled(float('-inf'))

        self.print_time_step(
            curr_state, pos_list[0], seq[:1], pos_list[:1])
        print("--------------------------------")

        best_path = []

        for i, color in enumerate(seq[1:]):
            # Get probability of evidence for each position
            # pos_prob = P(e_i|X_i)
            pos_prob = np.array([[self.floor_prob(color, x, y)
                                  for x in range(self.width)]
                                 for y in range(self.height)])

            pos_prob = np.ma.log(pos_prob).filled(float('-inf'))

            # init arrays to fill
            # next_prob = max[P(X_i | x_{i-1}) * max[P(x_{1...i-1} | e_{0:i})]]
            next_prob = [[float('-inf')
                          for _ in range(self.width)]
                         for _ in range(self.height)]

            # Save each step for backtracking path at end
            path_step = [[None
                          for _ in range(self.width)]
                         for _ in range(self.height)]

            for x in range(self.width):
                for y in range(self.height):
                    if self.is_floor((x, y)):
                        # tran_model = P(X_i | x_{i-1})
                        tran_model = self.generate_transition((x, y))

                        # curr_state = max[P(x_{1...i-1} | e_{0:i})]
                        # mult multiplies the two arrays
                        mult = np.array([[tran_model[y][x] * math.exp(curr_state[y][x])
                                          for x in range(self.width)]
                                         for y in range(self.height)])

                        # Get max value position
                        top_prob = np.argmax(mult)
                        path_step[y][x] = (top_prob % self.width,
                                           top_prob // self.width)

                        # Save max value
                        next_prob[y][x] = np.log(np.max(mult))

            # multiply probabilities
            pos_prob += np.array(next_prob)

            curr_state = self.normalize_log(pos_prob)
            best_path.append(path_step)

            self.print_time_step(
                curr_state, pos_list[i+1], seq[:i+2], pos_list[:i+2])
            print("--------------------------------")

        # Get most probably position and backtrack
        top_prob = np.argmax(curr_state)

        end_pos = (top_prob % self.width,
                   top_prob // self.width)

        return self.get_path(best_path, end_pos)

    # Backtrack to determine most likely sequence
    def get_path(self, best_path, end_pos):
        path = [end_pos]
        curr_pos = end_pos
        for path_step in best_path[::-1]:
            # Determine previous position
            x = curr_pos[0]
            y = curr_pos[1]
            curr_pos = path_step[y][x]

            path.append(curr_pos)

        path.reverse()
        return path

    # return P(e_i | x_i)
    def floor_prob(self, color, x, y):
        return 0 if not self.is_floor((x, y)) \
            else self.tpr if self.maze[y][x] == color \
            else self.fpr

    def is_floor(self, pos):
        if pos[0] < 0 or pos[0] >= self.width:
            return False
        if pos[1] < 0 or pos[1] >= self.height:
            return False

        return self.maze[pos[1]][pos[0]] != "#"

    def generate_transition(self, pos):
        # Get possible movements away from position
        prev_pos = {tuple(map(sum, zip(pos, move)))
                    for move in self.moves
                    if self.is_floor(tuple(map(sum, zip(pos, move))))}

        # 0.25 for adjacent floors
        # own position is 0.25 * every adjacent wall
        # 0 for all else
        tran_model = np.array([[0.25 if (x, y) in prev_pos
                                else 1 - (0.25 * self.transitions[y][x]) if (x, y) == pos
                                else 0
                                for x in range(self.width)]
                               for y in range(self.height)])

        return np.array(tran_model)

    # convert log probability to linear for output display
    def convert_probs(self, final_state):
        linear_state = np.array([[math.exp(x) for x in row]
                                 for row in final_state])
        return np.round(linear_state * 100, 1)

    # normalize logrithmic array of probabilites
    def normalize_log(self, curr_state):
        linear_state = np.array([[math.exp(x) for x in row]
                                 for row in curr_state])
        linear_state /= linear_state.sum()

        return np.ma.log(linear_state).filled(float('-inf'))

    # Output state at timestep
    # Not generalized to larger mazes well
    def print_time_step(self, curr_state, curr_pos, curr_color, curr_path):
        maze_output = "Scanned: '{}' at {}\n".format(
            curr_color[-1], curr_path[-1])
        maze_output += "Maze:\t\tProbabilities:\n"

        linear_state = self.convert_probs(curr_state)

        for i, row in enumerate(self.maze):
            # maze state
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

            # probability distribution
            for j, col in enumerate(linear_state[i]):
                if self.maze[i][j] == "#":
                    maze_output += "##" if j == 0 else " ##"
                else:
                    # "%02d" % col + str(col % 1)[1:3]
                    maze_output += " " + str(int(col)).zfill(2)

            maze_output += "\n\n"

        maze_output += "Scan history: {}\nCurrent path: {}".format(
            curr_color, curr_path)
        sleep(1)
        print(maze_output)


if __name__ == "__main__":

    colors = ["r", "g", "b", "y"]

    maze = HMMMaze(sys.argv[1], colors)

    seq, pos_list = maze.generate_sequence(int(sys.argv[3]))
    if int(sys.argv[2]) == 0:
        final_pos = maze.determine_seq(seq, pos_list)
        print("Guessed position: {}".format(final_pos))
    else:
        final_path = maze.determine_path(seq, pos_list)
        print("Guessed path: {}".format(final_path))
