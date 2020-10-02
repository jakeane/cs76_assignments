from SearchSolution import SearchSolution
from AStarQueue import AStarQueue
from heapq import heappush, heappop


class AstarNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state, heuristic, parent=None, transition_cost=0):
        self.state = state
        self.heuristic = heuristic
        self.parent = parent

        if parent:
            self.visited_cost = parent.visited_cost + transition_cost
        else:
            self.visited_cost = 0

    def priority(self):
        return self.visited_cost + self.heuristic

    # comparison operator,
    # needed for heappush and heappop to work with AstarNodes:
    def __lt__(self, other):
        return self.priority() < other.priority()


# take the current node, and follow its parents back
#  as far as possible. Grab the states from the nodes,
#  and reverse the resulting list of states.
def backchain(node):
    result = []
    current = node
    while current:
        result.append(current.state)
        current = current.parent

    result.reverse()
    return result


def astar_search(search_problem, heuristic_fn):
    # I'll get you started:
    start_node = AstarNode(search_problem.start_state,
                           heuristic_fn(search_problem.start_state))
    solution = SearchSolution(
        search_problem, "Astar with heuristic " + heuristic_fn.__name__)

    # init priority queue
    pqueue = AStarQueue()
    pqueue.add_node(start_node)

    # you write the rest:
    while pqueue.pq:
        # get next node
        curr_node = pqueue.pop_node()
        solution.nodes_visited += 1

        # get successors from state and iterate through
        successors = search_problem.get_successors(curr_node.state)
        for successor in successors:

            # check if robots moved
            # if not, transition cost is 0
            if curr_node.state[1:] == successor[1:]:
                succ_node = AstarNode(
                    successor, heuristic_fn(successor), curr_node, 0)
            else:
                succ_node = AstarNode(
                    successor, heuristic_fn(successor), curr_node, 1)

            # check if goal was reached
            if search_problem.goal_test(succ_node.state):
                solution.path = backchain(succ_node)
                solution.cost = succ_node.visited_cost
                return solution

            # 'attempt' to add successor to queue
            # see AStarQueue for behavior
            pqueue.add_node(succ_node)

    return solution
