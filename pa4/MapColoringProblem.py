from CSPNode import CSPNode
from collections import deque


class MapColoringProblem:

    def __init__(self, regions, borders, colors, var_select=0, sort_values=False):
        self.regions = {region: CSPNode(region, list(colors), set())
                        for region in regions}
        self.borders = borders
        for border in borders:
            self.regions[border[0]].neighbors.add(self.regions[border[1]])
            self.regions[border[1]].neighbors.add(self.regions[border[0]])

        self.var_select = var_select
        self.sort_values = sort_values
        self.assignments = dict()

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

    def solve(self):
        while not self.goal_test():
            region = self.mrv_heuristic()
            color = self.lcv_heuristic(region)
            region.domain = [color]
            self.assignments[region.name] = color
            print("Setting region {} domain to {}".format(
                region.name, region.domain))
            if not self.ac3():
                print("Failed to solve")
                break
            # print(self)
            print("---------")

    def backtracking_search(self):
        assignment = self.backtrack({})
        if assignment:
            print(assignment)
        else:
            print("Search failed")

    def backtrack(self, assignments):
        if self.goal_test(assignments):
            return assignments

        print(self)
        print("--------------")

        region = self.select_variable(assignments)

        values = region.domain
        if self.sort_values:
            values.sort(key=lambda value: self.lcv_h(
                region, value), reverse=True)

        for value in values:
            if self.check_consistent(region, value, assignments):
                assignments[region.name] = value
                save_domain = region.domain
                region.domain = [value]
                print("Setting region {} domain to {}".format(
                    region.name, region.domain))
                if self.ac3():
                    result = self.backtrack(assignments)

                    if result:
                        return assignments

                del assignments[region.name]
                region.domain = save_domain
                print("Reverting region {} domain to {}".format(
                    region.name, region.domain))

        return None

    def select_variable(self, assignments):
        if self.var_select == 1:
            return self.mrv_heuristic(assignments)
        elif self.var_select == 2:
            return self.degree_heuristic(assignments)

        for region in self.regions.values():
            if region.name not in assignments:
                return region

    def check_consistent(self, region, value, assignment):
        for neighbor in region.neighbors:
            if neighbor.name in assignment and assignment[neighbor.name] == value:
                return False
        return True

    def goal_test(self, assignments):
        return len(assignments) == len(self.regions)
        # success = True
        # for region in self.regions.values():
        #     if len(region.domain) > 1:
        #         success = False
        # return success

    def mrv_heuristic(self, assignments):
        result = None
        for region in self.regions.values():
            # if len(region.domain) > 1:
            if region.name not in assignments:
                if not result or len(region.domain) < len(result.domain):
                    result = region
        return result

    def degree_heuristic(self, assignments):
        result = None
        highest_degree = 0
        for region in self.regions.values():
            # if len(region.domain) > 1:
            if region.name not in assignments:
                curr_degree = 0
                for neighbor in region.neighbors:
                    # if len(neighbor.domain) > 1:
                    if neighbor.name not in assignments:
                        curr_degree += 1
                if curr_degree > highest_degree:
                    result = region
                    highest_degree = curr_degree

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

    def lcv_h(self, region, variable):
        curr_conflicts = 0
        for neighbor in region.neighbors:
            if variable in neighbor.domain:
                curr_conflicts += 1
        return curr_conflicts

    def ac3(self):
        saved_domain = {region.name: list(region.domain)
                        for region in self.regions.values()}
        arc_queue = deque(self.borders)

        while arc_queue:
            x_i, x_j = arc_queue.pop()
            if self.revise(x_i, x_j):
                if len(self.regions[x_i].domain) == 0 or len(self.regions[x_j].domain) == 0:
                    for region in self.regions.values():
                        region.domain = saved_domain[region.name]
                    return False
                for x_k in self.regions[x_i].neighbors:
                    if x_k.name == x_j:
                        continue
                    arc_queue.appendleft((x_k.name, x_i))
                for x_k in self.regions[x_j].neighbors:
                    if x_k.name == x_i:
                        continue
                    arc_queue.appendleft((x_k.name, x_j))
        return True

    def revise(self, x_i, x_j):
        revised = False

        for color in self.regions[x_i].domain:
            if len(self.regions[x_j].domain) == 1 and self.regions[x_j].domain[0] == color:
                # if self.assignments.get(self.regions[x_j].name, None) == color:
                print(
                    "Region {} domain {} <- removing {}".format(x_i, self.regions[x_i].domain, color))
                self.regions[x_i].domain.remove(color)
                revised = True
        for color in self.regions[x_j].domain:
            if len(self.regions[x_i].domain) == 1 and self.regions[x_i].domain[0] == color:
                # if self.assignments.get(self.regions[x_i].name, None) == color:
                print(
                    "Region {} domain {} <- removing {}".format(x_j, self.regions[x_j].domain, color))
                self.regions[x_j].domain.remove(color)
                revised = True

        return revised

    def __str__(self):
        output = ""
        for region in self.regions.values():
            output += "\n{}".format(region)
        return output


if __name__ == "__main__":
    regions = {"WA", "NT", "Q", "SA", "NSW", "V", "T"}
    borders = {("WA", "NT"), ("WA", "SA"), ("SA", "NT"), ("Q", "NT"), ("SA", "Q"),
               ("SA", "NSW"), ("SA", "V"), ("Q", "NSW"), ("V", "NSW")}
    colors = ["Red", "Green", "Blue"]

    # regions = {"A", "B", "C", "D", "E", "F", "G", "H", "I", "J"}
    # borders = {("A", "B"), ("A", "E"), ("A", "F"), ("G", "B"), ("C", "B"), ("C", "H"), ("C", "D"),
    #            ("D", "E"), ("D", "I"), ("E", "J"), ("F",
    #                                                 "I"), ("F", "H"), ("I", "G"),
    #            ("G", "J"), ("J", "H")}
    # colors = ["Red", "Green", "Blue"]

    map_problem = MapColoringProblem(regions, borders, colors)

    # print(map_problem)
    # print(map_problem.mrv_heuristic())
    # print(map_problem.degree_heuristic())
    # print(map_problem.lcv_heuristic(map_problem.regions["WA"]))

    # map_problem.solve()
    map_problem.backtracking_search()
