from math import log, sqrt
from Maze import Maze
from time import sleep


class SensorlessProblem:

    # You write the good stuff here:
    def __init__(self, maze):
        self.maze = maze
        # list comprehensions babyyyyyyyyyyy sorry grader
        self.start_state = (tuple([p
                                   for x in range(maze.width)
                                   for y in range(maze.height)
                                   if maze.is_floor(x, y)
                                   for p in (x, y)]))
        self.moves = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def __str__(self):
        string = "Blind robot problem: "
        return string

    def get_successors(self, state):
        # update maze
        self.maze.robotloc = list(state)

        successors = []

        # iterate through moves
        for move in self.moves:
            # a set allows 'copies' to be ignored in constant time
            new_succ = set()
            for loc in range(len(state) // 2):

                curr_loc = (state[2 * loc], state[2 * loc + 1])
                new_loc = tuple(map(sum, zip(curr_loc, move)))

                # if new position is valid, then the robot moves
                # so, make it the current position
                if self.maze.is_floor(new_loc[0], new_loc[1]):
                    curr_loc = new_loc

                new_succ.add(curr_loc)

            # flatten set of tuples into one large tuple
            successors.append(tuple(sum(new_succ, ())))

        return successors

    def transition_cost(self, a, b):
        return 1

    def goal_test(self, state):
        return len(state) == 2

    def compact_heuristic(self, state):
        # init values
        col_max = state[0]
        col_min = state[0]
        row_max = state[1]
        row_min = state[1]

        # iterate through state
        for curr_bot in range(len(state) // 2):
            # update maxes and mins
            col_max = max(col_max, state[2 * curr_bot])
            row_max = max(row_max, state[2 * curr_bot + 1])
            col_min = min(col_min, state[2 * curr_bot])
            row_min = min(row_min, state[2 * curr_bot + 1])

        # get ranges and return sum
        return (row_max - row_min) + (col_max - col_min)

    def colrow_heuristic(self, state):
        # sets to handle copies
        columns = set()
        rows = set()
        for curr_bot in range(len(state) // 2):
            columns.add(state[2 * curr_bot])
            rows.add(state[2 * curr_bot + 1])

        # -2 to guarantee it's admissable
        return len(columns) + len(rows) - 2

    def isolated_heuristic(self, state):
        res = 0
        for loc in range(len(state) // 2):
            curr_loc = (state[2 * loc], state[2 * loc + 1])

            # flag means that the current position is isolated
            flag = True
            for move in self.moves:
                new_loc = tuple(map(sum, zip(curr_loc, move)))
                for loc2 in range(len(state) // 2):
                    other_loc = (state[2 * loc2], state[2 * loc2 + 1])

                    # means a neighboring position was found, thus not isolated
                    if other_loc == new_loc:
                        flag = False

            if flag:
                res += 1
        return res

    def first_heuristic(self, state):
        return len(state) // 2

    # like compact_heuristic but the return value is the hypotenuse
    def pythagoras_compact_heuristic(self, state):
        col_max = state[0]
        col_min = state[0]
        row_max = state[1]
        row_min = state[1]
        for curr_bot in range(len(state) // 2):
            col_max = max(col_max, state[2 * curr_bot])
            row_max = max(row_max, state[2 * curr_bot + 1])
            col_min = min(col_min, state[2 * curr_bot])
            row_min = min(row_min, state[2 * curr_bot + 1])

        return sqrt((row_max - row_min)**2 + (col_max - col_min)**2)

    def log2_heuristic(self, state):
        return log(len(state) / 2, 2)

    def furthest_points_heuristic(self, state):
        max_dist = 0

        # point A
        for loc in range(len(state) // 2):
            curr_loc = (state[2 * loc], state[2 * loc + 1])

            # point B
            for loc2 in range(len(state) // 2):
                other_loc = (state[2 * loc2], state[2 * loc2 + 1])

                # Get distance between A and B
                distance = (curr_loc[0] - other_loc[0]) + \
                    (curr_loc[1] - other_loc[1])

                # update if larger
                max_dist = max(max_dist, distance)

        return max_dist

    def test_heuristic(self, state):
        return min(self.compact_heuristic(state), self.colrow_heuristic(state))

        # given a sequence of states (including robot turn), modify the maze and print it out.
        #  (Be careful, this does modify the maze!)

    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state)

        for state in path:
            print(str(self))
            self.maze.robotloc = tuple(state)
            sleep(0.4)

            print(str(self.maze))


# A bit of test code

if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    test_problem = SensorlessProblem(test_maze3)
