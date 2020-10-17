from CSPNode import CSPNode
from collections import deque


class MapColoringProblem:

    def __init__(self, variables, values, var_select=0, sort_values=False):
        self.variables = variables
        self.domains = {variable: list(values) for variable in variables}
        self.constraints = set()
        for variable in variables:
            for neighbor in variables[variable]:
                if (neighbor, variable) not in self.constraints:
                    self.constraints.add((variable, neighbor))
        self.var_select = var_select
        self.sort_values = sort_values

    def check_constraints(self):

        for variable in self.variables:
            if len(self.domains[variable]) == 0:
                return False
            elif len(self.domains[variable]) == 1:
                for neighbor in self.variables[variable]:
                    if len(self.domains[neighbor]) == 1 and \
                            self.domains[variable][0] == self.domains[neighbor][0]:
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

        variable = self.select_variable(assignments)

        domain = self.domains[variable]
        if self.sort_values:
            domain.sort(key=lambda value: self.lcv_h(
                variable, value), reverse=True)

        for value in domain:
            if self.check_consistent(variable, value, assignments):
                assignments[variable] = value
                save_domain = self.domains[variable]
                self.domains[variable] = [value]
                print("Setting region {} domain to {}".format(
                    variable, self.domains[variable]))
                if self.ac3():
                    result = self.backtrack(assignments)

                    if result:
                        return assignments

                del assignments[variable]
                self.domains[variable] = save_domain
                print("Reverting region {} domain to {}".format(
                    variable, self.domains[variable]))

        return None

    def select_variable(self, assignments):
        selection = None
        if self.var_select == 1:
            selection = self.mrv_heuristic(assignments)
        elif self.var_select == 2:
            selection = self.degree_heuristic(assignments)

        if not selection:
            for variable in self.variables:
                if variable not in assignments:
                    selection = variable
                    break
        return selection

    def check_consistent(self, variable, value, assignment):
        for neighbor in self.variables[variable]:
            if neighbor in assignment and assignment[neighbor] == value:
                return False
        return True

    def goal_test(self, assignments):
        return len(assignments) == len(self.variables)
        # success = True
        # for region in self.regions.values():
        #     if len(region.domain) > 1:
        #         success = False
        # return success

    def mrv_heuristic(self, assignments):
        selection = None
        for variable in self.domains:
            if variable not in assignments:
                if not selection or \
                        len(self.domains[variable]) < len(self.domains[selection]):
                    selection = variable
        return selection

    def degree_heuristic(self, assignments):
        selection = None
        highest_degree = 0
        for variable in self.variables:
            if variable not in assignments:
                curr_degree = 0
                for neighbor in self.variables[variable]:
                    if neighbor not in assignments:
                        curr_degree += 1
                if curr_degree > highest_degree:
                    selection = variable
                    highest_degree = curr_degree

        return selection

    def lcv_heuristic(self, variable):
        selection = None
        least_conflicts = float('inf')
        for value in self.domains[variable]:
            curr_conflicts = 0
            for neighbor in self.variables[variable]:
                if value in self.domains[neighbor]:
                    curr_conflicts += 1
            if curr_conflicts < least_conflicts:
                selection = value
                least_conflicts = curr_conflicts
        return selection

    def lcv_h(self, variable, value):
        curr_conflicts = 0
        for neighbor in self.variables[variable]:
            if value in self.domains[neighbor]:
                curr_conflicts += 1
        return curr_conflicts

    def ac3(self):
        # saved_domain = {region.name: list(region.domain)
        #                 for region in self.regions.values()}
        changelog = {variable: set() for variable in self.variables}
        arc_queue = deque(self.constraints)

        while arc_queue:
            x_i, x_j = arc_queue.pop()
            if self.revise(x_i, x_j, changelog):
                if len(self.domains[x_i]) == 0 or len(self.domains[x_j]) == 0:
                    for variable in changelog:
                        for value in changelog[variable]:
                            self.domains[variable].append(value)
                    return False
                for x_k in self.variables[x_i]:
                    if x_k == x_j:
                        continue
                    arc_queue.appendleft((x_k, x_i))
                for x_k in self.variables[x_j]:
                    if x_k == x_i:
                        continue
                    arc_queue.appendleft((x_k, x_j))
        return True

    def revise(self, x_i, x_j, changelog):
        revised = False

        for color in self.domains[x_i]:
            if len(self.domains[x_j]) == 1 and self.domains[x_j][0] == color:
                # if self.assignments.get(self.regions[x_j].name, None) == color:
                print(
                    "Region {} domain {} <- removing {}".format(x_i, self.domains[x_i], color))
                self.domains[x_i].remove(color)
                changelog[x_i].add(color)
                revised = True
        for color in self.domains[x_j]:
            if len(self.domains[x_i]) == 1 and self.domains[x_i][0] == color:
                # if self.assignments.get(self.domains[x_i].name, None) == color:
                print(
                    "Region {} domain {} <- removing {}".format(x_j, self.domains[x_j], color))
                self.domains[x_j].remove(color)
                changelog[x_j].add(color)
                revised = True

        return revised

    def __str__(self):
        output = ""
        for variable in self.variables:
            output += "Name: {}\n\tDomain: {}\n\tNeighbors:{}\n".format(
                variable, self.domains[variable], self.variables[variable])
        return output


if __name__ == "__main__":

    map_data = {
        "WA": ["SA", "NT"],
        "Q": ["SA", "NT", "NSW"],
        "T": [],
        "V": ["SA", "NSW"],
        "SA": ["V", "NT", "NSW", "WA", "Q"],
        "NT": ["SA", "WA", "Q"],
        "NSW": ["V", "SA", "Q"]
    }

    map_data = {
        "A": ["B", "E", "F"],
        "B": ["A", "G", "C"],
        "C": ["B", "D", "H"],
        "D": ["C", "E", "I"],
        "E": ["D", "A", "J"],
        "F": ["A", "H", "I"],
        "G": ["B", "J", "I"],
        "H": ["C", "F", "J"],
        "I": ["D", "F", "G"],
        "J": ["E", "G", "H"],
    }

    colors = ["Red", "Green", "Blue"]

    map_problem = MapColoringProblem(map_data, colors, 2, True)

    # print(map_problem)
    # print(map_problem.mrv_heuristic({}))
    # print(map_problem.degree_heuristic({}))
    # print(map_problem.lcv_heuristic("WA"))

    map_problem.backtracking_search()
