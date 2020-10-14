from CSPNode import CSPNode
from collections import deque


class MapColoringProblem:

    def __init__(self, regions, borders, colors):
        self.regions = {region: CSPNode(region, colors, {})
                        for region in regions}
        self.borders = borders
        for border in borders:
            self.regions[border[0]].neighbors.add(self.regions[border[1]])
            self.regions[border[1]].neighbors.add(self.regions[border[0]])
        self.colors = colors
        self.domains = {region: colors for region in regions}

    def check_constraints(self):

        for region in self.regions.values():
            if len(region.domain) == 0:
                return False
            elif len(region.domain) == 1:
                for neighbor in region.neighbors:
                    if len(neighbor.domain) == 1 and \
                            region.domain[0] == neighbor.domain[0]:
                        return False

        return True

    def mrv_heuristic(self):
        result = None
        for region in self.regions.values():
            if len(region.domain) > 1:
                if not result or len(region.domain) < len(result.domain):
                    result = region
        return result

    def degree_heuristic(self):
        result = None
        highest_degree = 0
        for region in self.regions.values():
            if len(region.domain) > 1:
                curr_degree = 0
                for neighbor in region.neighbors:
                    if len(neighbor.domain) > 1:
                        curr_degree += 1
                if curr_degree > highest_degree:
                    result = region

        return result

    def lcv_heuristic(self, region):
        result = None
        least_conflicts = float('inf')
        for variable in region.domain:
            curr_conflicts = 0
            for neighbor in region.neighbors:
                if variable in neighbor.domain:
                    curr_conflicts += 1
            if curr_conflicts < least_conflicts:
                result = variable
        return result

    def ac3(self):
        pass
