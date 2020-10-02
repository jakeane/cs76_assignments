import itertools
from heapq import heappop, heappush

# Modified from provided documentation
# https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes


class AStarQueue:

    def __init__(self):
        self.pq = []                         # list of entries arranged in a heap
        self.entry_finder = {}               # mapping of nodes to entries

    def add_node(self, node):
        # Add node if not visited or 'lower' priority
        if node.state in self.entry_finder:
            if self.entry_finder[node.state][0] > node:
                self.remove_node(node)
                entry = [node, False]
                self.entry_finder[node.state] = entry
                heappush(self.pq, node)
        else:
            entry = [node, False]
            self.entry_finder[node.state] = entry
            heappush(self.pq, node)

    # Mark node as removed to allow addition of 'better' node
    def remove_node(self, node):
        self.entry_finder[node.state][-1] = True

    def pop_node(self):
        'Remove and return the lowest priority node. Raise KeyError if empty.'
        while self.pq:
            node = heappop(self.pq)
            if not self.entry_finder[node.state][1]:
                return node
        raise KeyError('pop from an empty priority queue')
