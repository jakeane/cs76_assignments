from collections import deque


class ConstraintSatisfactionProblem:

    def __init__(self, variables, values, infer=False, var_select=0, sort_values=False):
        self.variables = dict()
        self.domains = dict()
        self.infer = infer
        self.var_select = var_select
        self.sort_values = sort_values
        self.constraints = set()
        self.visits = 0

    def backtracking_search(self):
        assignments = self.backtrack({})
        if assignments:
            output = "After searching {} nodes. The following assignments were satisfactory:".format(
                self.visits)
            for variable in assignments:
                output += "\n - Variable {} assigned value {}".format(
                    variable, assignments[variable])
            print(output)

        else:
            print("After searching {} nodes, the search failed".format(self.visits))

    def backtrack(self, assignments):
        self.visits += 1
        if self.goal_test(assignments):
            return assignments

        variable = self.select_variable(assignments)

        domain = self.domains[variable]
        if self.sort_values:
            domain.sort(
                key=lambda value: self.lcv_heuristic(variable, value))

        for value in domain:
            if self.check_consistent(variable, value):
                assignments[variable] = value
                changelog = {variable: set() for variable in self.variables}
                changelog[variable] = set(self.domains[variable])
                changelog[variable].remove(value)
                self.domains[variable] = [value]

                if not (self.infer and not self.ac3(changelog)):
                    result = self.backtrack(assignments)

                    if result:
                        return assignments

                del assignments[variable]
                for changed_var in changelog:
                    for value in changelog[changed_var]:
                        self.domains[changed_var].append(value)

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

    def goal_test(self, assignments):
        return len(assignments) == len(self.variables)

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
                curr_degree = self.get_degree(variable, assignments)
                if curr_degree > highest_degree:
                    selection = variable
                    highest_degree = curr_degree

        return selection

    def get_degree(self, variable, assignments):
        return 1

    def lcv_heuristic(self, var_b, val_b):
        conflicts = 0
        for var_a in self.variables[var_b]:
            for val_a in self.domains[var_a]:
                if self.constraint_helper(var_a, var_b, val_a, val_b):
                    conflicts += 1
        return conflicts

    def ac3(self, changelog):
        arc_queue = deque(self.constraints)

        while arc_queue:
            var_a, var_b = arc_queue.pop()
            if self.revise(var_a, var_b, changelog):
                if len(self.domains[var_a]) == 0 or len(self.domains[var_b]) == 0:
                    return False
                for var_c in self.variables[var_a]:
                    if var_c == var_b:
                        continue
                    arc_queue.appendleft((var_c, var_a))
                for var_c in self.variables[var_b]:
                    if var_c == var_a:
                        continue
                    arc_queue.appendleft((var_c, var_b))
        return True

    def revise(self, var_a, var_b, changelog):
        revised = False

        for value in self.domains[var_a]:
            if self.constraint_unsatisfiable(var_b, var_a, value):
                self.domains[var_a].remove(value)
                changelog[var_a].add(value)
                revised = True
        for value in self.domains[var_b]:
            if self.constraint_unsatisfiable(var_a, var_b, value):
                self.domains[var_b].remove(value)
                changelog[var_b].add(value)
                revised = True

        return revised

    def check_consistent(self, variable, value):
        for neighbor in self.variables[variable]:
            if self.constraint_unsatisfiable(neighbor, variable, value):
                return False
        return True

    def constraint_unsatisfiable(self, var_a, var_b, value):
        if len(self.domains[var_a]) == 1:
            val_a = self.domains[var_a][0]
            return self.constraint_helper(var_a, var_b, val_a, value)
        return False

    def constraint_helper(self, var_a, var_b, val_a, val_b):
        return False

    def __str__(self):
        output = ""
        for variable in self.variables:
            output += "Name: {}\n\tDomain: {}\n\tNeighbors:{}\n".format(
                variable, self.domains[variable], self.variables[variable])
        return output
