from MazeworldProblem import MazeworldProblem
from Maze import Maze

# from uninformed_search import bfs_search
from astar_search import astar_search

# null heuristic, useful for testing astar search without heuristic (uniform cost search).


def null_heuristic(state):
    return 0

# Test problems


# Load mazes
test_maze3 = Maze("maze3.maz")
test_maze4 = Maze("maze4.maz")
test_maze5 = Maze("maze5.maz")
test_maze6 = Maze("maze6.maz")
test_maze7 = Maze("maze7.maz")
test_maze8 = Maze("maze8.maz")

# Maze 3
test_mp = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))
result = astar_search(test_mp, test_mp.manhattan_heuristic)
print(result)
test_mp.animate_path(result.path)

# Maze 4
test_mp = MazeworldProblem(test_maze4, (6, 1, 5, 1, 4, 1))
result = astar_search(test_mp, test_mp.manhattan_heuristic)
print(result)
test_mp.animate_path(result.path)

# Maze 5
test_mp = MazeworldProblem(test_maze5, (5, 3, 0, 1, 4, 2))
result = astar_search(test_mp, test_mp.manhattan_heuristic)
print(result)
test_mp.animate_path(result.path)

# Maze 6
test_mp = MazeworldProblem(test_maze6, (9, 10, 8, 6))
result = astar_search(test_mp, test_mp.manhattan_heuristic)
print(result)
test_mp.animate_path(result.path)

# Maze 7
test_mp = MazeworldProblem(test_maze7, (29, 1, 35, 3))
result = astar_search(test_mp, test_mp.manhattan_heuristic)
print(result)
test_mp.animate_path(result.path)
