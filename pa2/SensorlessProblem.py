from Maze import Maze
from time import sleep


class SensorlessProblem:

    # You write the good stuff here:
    def __init__(self, maze, start_spot):
        self.maze = maze
        self.location = start_spot
        # list comprehensions babyyyyyyyyyyy sorry
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
        self.maze.robotloc = list(state)

        successors = []

        for move in self.moves:
            new_succ = set()
            for loc in range(len(state) // 2):
                curr_loc = (state[2 * loc], state[2 * loc + 1])
                # print(curr_loc)

                new_loc = tuple(map(sum, zip(curr_loc, move)))

                if self.maze.is_floor(new_loc[0], new_loc[1]):
                    curr_loc = new_loc
                new_succ.add(curr_loc)
            successors.append(tuple(sum(new_succ, ())))
            # print("move:" + str(move))
            # print(new_succ)
            # successors.append(new_succ)

        # print(successors)
        return successors

    def transition_cost(self, a, b):
        return 1

    def goal_test(self, state):
        return len(state) == 2

    def sensorless_heuristic(self, state):
        return len(state) // 2

    def colrow_heuristic(self, state):
        columns = set()
        rows = set()
        for curr_bot in range(len(state) // 2):
            columns.add(state[2 * curr_bot])
            rows.add(state[2 * curr_bot + 1])

        return min(len(columns) + len(rows), len(state)) / 2

    def blob_heuristic(self, state):
        res = 0
        for loc in range(len(state) // 2):
            curr_loc = (state[2 * loc], state[2 * loc + 1])
            flag = True
            for move in self.moves:
                new_loc = tuple(map(sum, zip(curr_loc, move)))
                for loc2 in range(len(state) // 2):
                    other_loc = (state[2 * loc2], state[2 * loc2 + 1])
                    if other_loc == new_loc:
                        flag = False

            if flag:
                res += 1
        return res

    def test_heuristic(self, state):
        return 0

        # given a sequence of states (including robot turn), modify the maze and print it out.
        #  (Be careful, this does modify the maze!)

    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state)

        for state in path:
            print(str(self))
            self.maze.robotloc = tuple(state)
            sleep(1)

            print(str(self.maze))


# A bit of test code

if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    test_problem = SensorlessProblem(test_maze3)
