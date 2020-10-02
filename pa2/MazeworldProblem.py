from Maze import Maze
from time import sleep
from math import sqrt


class MazeworldProblem:

    # you write the constructor, and whatever methods your astar function needs

    def __init__(self, maze, goal_locations):
        self.maze = maze
        self.start_state = tuple([0] + maze.robotloc)
        self.num_bots = len(goal_locations) // 2
        self.goal_locations = goal_locations
        self.moves = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def __str__(self):
        string = "Mazeworld problem: "
        return string

    def get_successors(self, state):
        # update maze to current state
        self.maze.robotloc = list(state[1:])

        # derive relevant factors from state
        curr_bot = state[0]
        curr_pos = state[2 * curr_bot + 1: 2 * curr_bot + 3]
        next_bot = (curr_bot + 1) % self.num_bots

        # init with case where bots do not move
        successors = [tuple([next_bot])+state[1:]]

        for move in self.moves:
            # calculate new position by 'adding' the tuples
            new_pos = tuple(map(sum, zip(curr_pos, move)))

            # check if new position is valid
            if self.maze.is_floor(new_pos[0], new_pos[1]) and not self.maze.has_robot(new_pos[0], new_pos[1]):
                # build new successor and add to list
                new_succ = tuple([next_bot]) + \
                    state[1:2 * curr_bot + 1] + \
                    new_pos + \
                    state[2 * curr_bot + 3:]
                successors.append(new_succ)
        return successors

    def goal_test(self, state):
        return self.goal_locations == state[1:]

    def euclidian_heuristic(self, state):
        heuristic = 0
        for curr_bot in range(self.num_bots):
            x_diff = abs(
                self.goal_locations[2 * curr_bot] - state[2 * curr_bot + 1])
            y_diff = abs(
                self.goal_locations[2 * curr_bot + 1] - state[2 * curr_bot + 2])

            heuristic += sqrt(x_diff**2 + y_diff**2)

        return heuristic

    def manhattan_heuristic(self, state):
        heuristic = 0
        for curr_bot in range(self.num_bots):
            heuristic += abs(
                self.goal_locations[2 * curr_bot] - state[2 * curr_bot + 1])
            heuristic += abs(
                self.goal_locations[2 * curr_bot + 1] - state[2 * curr_bot + 2])

        return heuristic

        # given a sequence of states (including robot turn), modify the maze and print it out.
        #  (Be careful, this does modify the maze!)

    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state[1:])

        for state in path:
            print(str(self))
            self.maze.robotloc = tuple(state[1:])
            sleep(1)

            print(str(self.maze))


# A bit of test code. You might want to add to it to verify that things
#  work as expected.

if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    test_mp = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))

    print(test_mp.get_successors((2, 1, 0, 1, 1, 2, 1)))
