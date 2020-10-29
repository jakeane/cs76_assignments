from Logic import Logic
from display import display_sudoku_solution
import random
from collections import deque
import sys


class SAT(Logic):

    def __init__(self, cnf_filename, threshold=0.7):
        super().__init__(cnf_filename)
        self.threshold = threshold

    # Key differences between GSAT and WalkSAT is the selection method
    # of the variable and the limit. Thus they are parameters for
    # a generic SAT.
    def gsat(self):
        return self.generic_sat(200000, self.gsat_list)

    def walksat(self):
        return self.generic_sat(100000, self.walksat_list)

    def gsat_list(self):
        return {i: variable for i, variable in enumerate(self.variables)}

    def walksat_list(self):
        return random.choice([clause
                              for clause in self.clauses
                              if not self.clause_valid(clause)])

    def generic_sat(self, limit, var_list):
        counter = 0
        satisfied = self.count_satisfied_clauses()

        while satisfied != len(self.clauses) and counter < limit:
            random.seed()
            print(satisfied, counter)

            # Select and flip variable
            variable, net_satisfied = self.choose_variable(var_list())
            self.variables[variable] = not self.variables[variable]

            # Update number of satisfied clauses
            satisfied += net_satisfied
            counter += 1

        return self.count_satisfied_clauses() == len(self.clauses)

    def choose_variable(self, variable_list):
        # Random choice
        if random.random() > self.threshold:
            variable = random.choice(list(variable_list))
            net_satisfied = self.score_variable(variable)

        # 'Determined' choice
        else:
            most_satisfied_var = []
            net_satisfied = float('-inf')

            for variable in variable_list:
                curr_satisfied = self.score_variable(variable)

                # If new best
                if curr_satisfied > net_satisfied:
                    most_satisfied_var = [variable]
                    net_satisfied = curr_satisfied

                # If equal to best
                elif curr_satisfied == net_satisfied:
                    most_satisfied_var.append(variable)

            # Select from best variables
            variable = random.choice(most_satisfied_var)

        return variable, net_satisfied

    def count_satisfied_clauses(self):
        satisfied = 0
        for clause in self.clauses:
            if self.clause_valid(clause):
                satisfied += 1
        return satisfied

    def score_variable(self, variable):

        # Calculate how many clauses are satisfied in variables's
        # domain before flipping.
        curr_satisfied = 0
        for clause in self.domains[variable]:
            if self.clause_valid(clause):
                curr_satisfied += 1

        self.variables[variable] = not self.variables[variable]

        # Calculate how many clauses are satisfied in variables's
        # domain after flipping.
        satisfied = 0
        for clause in self.domains[variable]:
            if self.clause_valid(clause):
                satisfied += 1

        self.variables[variable] = not self.variables[variable]

        # return 'net' satisfied
        return satisfied - curr_satisfied

    def clause_valid(self, clause):
        for variable in clause:
            if self.variables[variable] == clause[variable]:
                return True
        return False


if __name__ == "__main__":
    sat = SAT(sys.argv[1])
    sat.walksat()
    print(sat.variables)
