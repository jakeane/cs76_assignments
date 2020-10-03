import itertools
from heapq import heappop, heappush

# Modified from provided documentation
# https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes


class AStarQueue:

    def __init__(self):
        self.pq = []                         # list of entries arranged in a heap
        self.entry_finder = {}               # mapping of nodes to entries

    def add_node(self, node):
        # push node if not visited or 'lower' priority
        if node.state in self.entry_finder:
            if self.entry_finder[node.state][0] > node:
                self.remove_node(node)
                self.push_node(node)
        else:
            self.push_node(node)

    def push_node(self, node):
        entry = [node, False]
        self.entry_finder[node.state] = entry
        heappush(self.pq, entry)

    # Mark node as removed to allow addition of 'better' node
    def remove_node(self, node):
        entry = self.entry_finder.pop(node.state)
        entry[-1] = True

    def pop_node(self):
        'Remove and return the lowest priority node. Raise KeyError if empty.'
        while self.pq:
            node, removed = heappop(self.pq)
            if not removed:
                return node
        raise KeyError('pop from an empty priority queue')
