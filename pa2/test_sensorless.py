# You write this:
from SensorlessProblem import SensorlessProblem
from Maze import Maze
from astar_search import astar_search

test_maze3 = Maze("maze3.maz")
test_maze4 = Maze("maze4.maz")
test_maze5 = Maze("maze5.maz")
test_maze6 = Maze("maze6.maz")
test_maze7 = Maze("maze7.maz")
test_maze8 = Maze("maze8.maz")

test_sp = SensorlessProblem(test_maze3)
result = astar_search(test_sp, test_sp.compact_heuristic)
print(result)
# test_sp.animate_path(result.path)

test_sp = SensorlessProblem(test_maze4)
result = astar_search(test_sp, test_sp.compact_heuristic)
print(result)
# test_sp.animate_path(result.path)

test_sp = SensorlessProblem(test_maze5)
result = astar_search(test_sp, test_sp.compact_heuristic)
print(result)
test_sp.animate_path(result.path)

test_sp = SensorlessProblem(test_maze8)
result = astar_search(test_sp, test_sp.compact_heuristic)
print(result)
# test_sp.animate_path(result.path)
