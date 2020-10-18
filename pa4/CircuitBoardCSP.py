from ConstraintSatisfactionProblem import ConstraintSatisfactionProblem
from time import sleep


class CircuitBoardCSP(ConstraintSatisfactionProblem):

    def __init__(self, variables, values, infer=False, var_select=0, sort_values=False):
        super().__init__(variables, values, infer, var_select, sort_values)

        # values is actually board size, actual values are inferred
        self.size = values

        # init data to int mapping
        self.var_conv = {var: id for id, var in enumerate(variables)}

        self.variables = {variable: [neighbor
                                     for neighbor in range(len(variables))
                                     if neighbor != variable]
                          for variable in range(len(variables))}

        self.dom_conv = {y*self.size[0] + x: (x, y)
                         for y in range(self.size[1])
                         for x in range(self.size[0])}

        # given size of board and component, domains are inferred
        self.domains = {self.var_conv[variable]: [x + y*self.size[0]
                                                  for y in range(self.size[1])
                                                  for x in range(self.size[0])
                                                  if self.can_fit(variable, (x, y))]
                        for variable in variables}

        # constraints
        for var_a in self.variables:
            for var_b in self.variables:
                # note that reversed tuple in condition prevents duplicates
                if var_a != var_b and (var_b, var_a) not in self.constraints:
                    self.constraints.add((var_a, var_b))

        # flip variable conversion to allow int to data translation
        self.var_conv = {id: var for var, id in self.var_conv.items()}

    # helper to determine where components can/cannot fit
    def can_fit(self, variable, value):
        if value[0] + variable[0] > self.size[0] or value[1] + variable[1] > self.size[1]:
            return False
        return True

    # print board before entering parent function
    def backtrack(self, assignments):
        self.print_board(assignments)
        return super().backtrack(assignments)

    # degree determined by size of variable
    def get_degree(self, variable, assignments):
        return self.var_conv[variable][0] * self.var_conv[variable][1]

    # returns true if components overlap, as that is not allowed
    def constraint_helper(self, var_a, var_b, val_a, val_b):

        # for code readability
        conv_var_a = self.var_conv[var_a]
        conv_var_b = self.var_conv[var_b]
        conv_val_a = self.dom_conv[val_a]
        conv_val_b = self.dom_conv[val_b]

        if (conv_val_a[0] >= conv_val_b[0] + conv_var_b[0] or
                conv_val_a[0] + conv_var_a[0] <= conv_val_b[0]):
            return False

        if (conv_val_a[1] >= conv_val_b[1] + conv_var_b[1] or
                conv_val_a[1] + conv_var_a[1] <= conv_val_b[1]):
            return False

        return True

    def print_board(self, assignments):
        output = ""
        occupied = {}

        # map positions to components by iterating through each component
        for num, variable in enumerate(assignments):
            for x in range(self.var_conv[variable][0]):
                for y in range(self.var_conv[variable][1]):
                    pos = self.dom_conv[assignments[variable]]
                    occupied[(pos[0]+x, pos[1]+y)] = chr(ord("A") + num)

        # build output
        for y in range(self.size[1]-1, -1, -1):
            for x in range(self.size[0]):
                # returns '.' if key not found, meaning it's empty
                output += occupied.get((x, y), ".")
            output += "\n"
        print(output)
        sleep(0.25)


if __name__ == "__main__":

    circuit_data = {(3, 2), (5, 2), (2, 3), (7, 1)}

    circuit_data = {(7, 1), (3, 2), (5, 2), (2, 3)}

    positions = (10, 3)

    # circuit_data = {(2, 2), (3, 2), (4, 1), (4, 2), (1, 3)}
    # positions = (5, 5)

    circuit_problem = CircuitBoardCSP(
        circuit_data, positions, infer=True, var_select=2, sort_values=True)

    # print(circuit_problem)
    # print(circuit_problem.mrv_heuristic({}))
    # print(circuit_problem.degree_heuristic({}))
    # print(circuit_problem.lcv_heuristic((2, 3)))

    # circuit_problem.domains[(3, 2)] = [(4, 0)]
    # print(circuit_problem.constraint_unsatisfiable((3, 2), (5, 2), (1, 0)))
    circuit_problem.backtracking_search()

    # output = ""
    # for val_a in circuit_problem.domains[(3, 2)]:
    #     for val_b in circuit_problem.domains[(5, 2)]:
    #         if not circuit_problem.constraint_helper((3, 2), (5, 2), val_a, val_b):
    #             output += "[{}, {}], ".format(val_a, val_b)
    # print(output)
