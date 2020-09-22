
from collections import deque
from SearchSolution import SearchSolution
from FoxProblem import FoxProblem

# you might find a SearchNode class useful to wrap state objects,
#  keep track of current depth for the dfs, and point to parent nodes


class SearchNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent

    def __str__(self):
        return "State: " + str(self.state) + ". Parent: " + str(self.parent.state if self.parent else " ")


# you might write other helper functions, too. For example,
#  I like to separate out backchaining, and the dfs path checking functions


def backchain(curr_node):
    chain = [curr_node.state]

    while curr_node.parent:
        curr_node = curr_node.parent
        chain.insert(0, curr_node.state)

    return chain


def bfs_search(search_problem):
    # init problem
    solution = SearchSolution(search_problem, "BFS")
    visited = {search_problem.start_state}
    queue = deque([SearchNode(search_problem.start_state)])

    while queue:
        curr_node = queue.pop()

        # if goal found, get path and break loop
        if search_problem.goal_test(curr_node.state):
            solution.path = backchain(curr_node)
            break

        # add all non-visited successors to data structures
        for successor in search_problem.get_successors(curr_node.state):
            if successor not in visited:
                queue.appendleft(SearchNode(successor, curr_node))
                visited.add(successor)

    solution.nodes_visited = len(visited)
    return solution


# Don't forget that your dfs function should be recursive and do path checking,
#  rather than memoizing (no visited set!) to be memory efficient

# We pass the solution along to each new recursive call to dfs_search
#  so that statistics like number of nodes visited or recursion depth
#  might be recorded


def dfs_search(search_problem, depth_limit=100, node=None, solution=None):
    # if no node object given, create a new search from starting state
    if node == None:
        node = SearchNode(search_problem.start_state)
        solution = SearchSolution(search_problem, "DFS")

    solution.nodes_visited += 1

    # return if depth limit reached
    if depth_limit == 0:
        return solution

    for successor in search_problem.get_successors(node.state):
        if successor not in backchain(node):

            # if goal is reached, get path and return
            if search_problem.goal_test(successor):
                solution.path = backchain(SearchNode(successor, node))
                return solution

            # get new solution
            solution = dfs_search(
                search_problem, depth_limit - 1, SearchNode(successor, node), solution)

            # if path is not empty, then goal was reached in recursion
            # so, return solution
            if len(solution.path) > 0:
                return solution

    return solution


def ids_search(search_problem, depth_limit=100):
    # init solution
    solution = SearchSolution(search_problem, "IDS")

    for i in range(depth_limit):
        # attempt to find solution, record visited nodes
        possible_solution = dfs_search(search_problem, i)
        solution.nodes_visited += possible_solution.nodes_visited

        # if path is not empty, then goal was reached in iteration
        # so, break from loop and return solution
        if len(possible_solution.path) > 0:
            solution.path = possible_solution.path
            break

    return solution


if __name__ == "__main__":
    test_cp = FoxProblem((5, 4, 1))
    print(bfs_search(test_cp))
    print(dfs_search(test_cp))
    print(ids_search(test_cp))
