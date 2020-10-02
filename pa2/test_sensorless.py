# You write this:
from SensorlessProblem import SensorlessProblem
from Maze import Maze
from astar_search import astar_search

test_maze = Maze("maze5.maz")

test_sp = SensorlessProblem(test_maze, (1, 1))
# print(test_sp.start_state)
# print(test_sp.get_successors(test_sp.start_state))


def null_heuristic(state):
    return 0


result = astar_search(test_sp, null_heuristic)
print(result)
# test_sp.animate_path(result.path)


result = astar_search(test_sp, test_sp.sensorless_heuristic)
print(result)
# test_sp.animate_path(result.path)

# result = astar_search(test_sp, test_sp.colrow_heuristic)
# print(result)
# test_sp.animate_path(result.path)
