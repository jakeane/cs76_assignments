from display import display_sudoku_solution
import random
import sys


class SAT:

    def __init__(self, cnf_filename, threshold=0.7):

        self.variables = [False]
        self.encode = dict()
        self.threshold = threshold
        self.read_cnf(cnf_filename)

    def read_cnf(self, cnf_filename):
        cnf = open(cnf_filename)

        self.clauses = [{self.encode_var(term): term[0] != "-"
                         for term in clause.split()}
                        for clause in cnf]

        self.domains = {variable: [clause
                                   for clause in self.clauses
                                   if variable in clause]
                        for variable in range(len(self.variables))}

        cnf.close()

    def encode_var(self, term):
        if term[0] == "-":
            term = term[1:]

        if term not in self.encode:
            self.encode[term] = len(self.variables)
            self.variables.append(bool(random.getrandbits(1)))

        return self.encode[term]

    def gsat(self):
        return self.generic_sat(200000, self.gsat_list)

    def walksat(self):
        return self.generic_sat(100000, self.walksat_list)

    def gsat_list(self):
        return self.variables

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

            variable, net_satisfied = self.choose_variable(var_list())

            self.variables[variable] = not self.variables[variable]

            satisfied += net_satisfied
            counter += 1

        return self.count_satisfied_clauses() == len(self.clauses)

    def choose_variable(self, variable_list):
        if random.random() > self.threshold:
            variable = random.choice(list(variable_list))
            net_satisfied = self.score_variable(variable)

        else:
            most_satisfied_var = []
            net_satisfied = float('-inf')

            for variable in variable_list:
                curr_satisfied = self.score_variable(variable)
                if curr_satisfied > net_satisfied:
                    most_satisfied_var = [variable]
                    net_satisfied = curr_satisfied
                elif curr_satisfied == net_satisfied:
                    most_satisfied_var.append(variable)

            variable = random.choice(most_satisfied_var)

        return variable, net_satisfied

    def count_satisfied_clauses(self):
        satisfied = 0
        for clause in self.clauses:
            if self.clause_valid(clause):
                satisfied += 1
        print(satisfied)
        return satisfied

    def score_variable(self, variable):

        curr_satisfied = 0
        for clause in self.domains[variable]:
            if self.clause_valid(clause):
                curr_satisfied += 1
            else:
                curr_satisfied -= 1

        self.variables[variable] = not self.variables[variable]

        satisfied = 0
        for clause in self.domains[variable]:
            if self.clause_valid(clause):
                satisfied += 1
            else:
                satisfied -= 1

        self.variables[variable] = not self.variables[variable]

        return int((satisfied - curr_satisfied) / 2)

    def clause_valid(self, clause):
        for variable in clause:
            if self.variables[variable] == clause[variable]:
                return True
        return False

    def write_solution(self, sol_filename):
        decode = {value: key for key, value in self.encode.items()}

        solution = open(sol_filename, "w")
        for i, variable in enumerate(self.variables):
            if variable:
                solution.write("{}\n".format(decode[i]))

        solution.close()


if __name__ == "__main__":
    sat = SAT(sys.argv[1])
    print(sat.walksat())
