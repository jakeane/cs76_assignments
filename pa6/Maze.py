from operator import pos
import random
import numpy as np
import math


class Maze:

    def __init__(self, width, height, colors):
        self.width = width
        self.height = height

        random.seed()
        self.floor_colors = np.array([[random.choice(colors)
                                       for _ in range(width)]
                                      for _ in range(height)])

        self.pos_probs = np.array([[math.log(1 / (width * height))
                                    for _ in range(width)]
                                   for _ in range(height)])

        self.tran_model = np.array([[random.choice(colors)
                                     for _ in range(width)]
                                    for _ in range(height)])

        self.moves = [(1, 0), (0, 1), (-1, 0), (0, -1), (0, 0)]

    def generate_sequence(self, total_moves=10):
        random.seed()
        curr_pos = (random.choice(range(self.width)),
                    random.choice(range(self.height)))

        seq = [self.floor_colors[curr_pos[0]][curr_pos[1]]]
        pos_list = [curr_pos]

        for _ in range(total_moves):
            move = random.choice(self.moves)
            new_pos = tuple(map(sum, zip(curr_pos, move)))
            if self.is_floor(new_pos):
                curr_pos = new_pos
            seq.append(self.floor_colors[curr_pos[0]][curr_pos[1]])
            pos_list.append(curr_pos)

        self.seq = seq
        self.pos_list = pos_list

    def determine_seq(self):
        # color = "r"
        curr_state = np.array([[self.floor_prob(self.seq[0], x, y)
                                for x in range(self.width)]
                               for y in range(self.height)])
        curr_state /= curr_state.sum()
        curr_state = np.log(curr_state)
        # print(curr_state)
        # print("-------------")

        for color in self.seq[1:]:
            pos_prob = np.array([[self.floor_prob(color, x, y)
                                  for x in range(self.width)]
                                 for y in range(self.height)])

            pos_prob /= pos_prob.sum()
            pos_prob = np.log(pos_prob)

            next_prob = [[None
                          for x in range(self.width)]
                         for y in range(self.height)]

            for x in range(self.width):
                for y in range(self.height):
                    tran_model = self.generate_transition((y, x))

                    mult = np.array([[self.mult_tran(tran_model, curr_state, x, y)
                                      for x in range(self.width)]
                                     for y in range(self.height)])
                    # print(mult)
                    next_prob[y][x] = np.max(mult)
                    # print("---")
                    # print(next_prob)
                    # print("---")

            pos_prob += np.array(next_prob)
            # print("---")
            # print(np.array(next_prob))
            # print("---")
            # print(pos_prob)
            # print("-------------")
            curr_state = pos_prob
            print("-------------")
            print(self.floor_colors)
            print(self.seq)
            print(color)
            print(self.convert_probs(curr_state))
            print("-------------")

        return curr_state
        # print(curr_prob)

        # test = np.array([[1 for x in range(self.width)]
        #                  for y in range(self.height)])

        # print(test)
        # print(test * curr_prob)

    def floor_prob(self, color, x, y):
        return 0.88 if self.floor_colors[y][x] == color else 0.04

    def is_floor(self, pos):
        return 0 <= pos[0] < self.width and 0 <= pos[1] < self.height

    def generate_transition(self, pos):
        prev_pos = set()
        for move in self.moves:
            new_pos = tuple(map(sum, zip(pos, move)))
            if self.is_floor(new_pos):
                prev_pos.add(new_pos)

        tran_model = np.array([[1 / len(prev_pos) if (y, x) in prev_pos else 0
                                for x in range(self.width)]
                               for y in range(self.height)])

        # curr_state = np.array([[self.floor_prob(self.seq[0], x, y)
        #                         for x in range(self.width)]
        #                        for y in range(self.height)])

        # mult = np.array([[self.mult_tran(tran_model, curr_state, x, y)
        #                   for x in range(self.width)]
        #                  for y in range(self.height)])

        return tran_model

    def mult_tran(self, tran_model, state_model, x, y):
        if tran_model[y][x] == 0:
            return float('-inf')
        else:
            return np.log(tran_model[y][x]) + state_model[y][x]

    def convert_probs(self, final_state):
        linear_state = np.array([[math.exp(x) for x in row]
                                 for row in final_state])
        return np.round(linear_state / linear_state.sum() * 100, 1)


if __name__ == "__main__":

    width = 4
    height = 4
    colors = ["r", "g", "b", "y"]

    maze = Maze(width, height, colors)

    print(maze.floor_colors)
    maze.generate_sequence(10)
    print(maze.seq)
    final_state = maze.determine_seq()
    # maze.convert_probs(final_state)
    # print(maze.generate_transition((2, 0)))

    arr1 = np.array([[1, 2], [5, 4]])
    print(np.max(arr1))
    # # arr2 = np.array([[4, 2], [1, 8]])

    # print(arr1 / arr1.sum())
    # print(np.log(arr1 / arr1.sum()))
