import random


class Logic:
    def __init__(self, cnf_filename):

        # Variables Format
        # [True, False, False, ...]
        self.variables = []
        self.encode = dict()
        self.read_cnf(cnf_filename)

    def read_cnf(self, cnf_filename):
        cnf = open(cnf_filename)

        # Clause Format:
        # [{0: False, 1: True}, {1: False, 24: False, 12: True}, ...]
        self.clauses = [{self.encode_var(term): term[0] != "-"
                         for term in clause.split()}
                        for clause in cnf]

        # Helped optimize SAT by limiting number of clauses viewed.
        # When evaluating a variable, you only need to look at clauses
        # that are affected by the variable.
        self.domains = {variable: [clause
                                   for clause in self.clauses
                                   if variable in clause]
                        for variable in range(len(self.variables))}

        cnf.close()

    # returns index in variables list
    def encode_var(self, term):
        # Remove negation
        if term[0] == "-":
            term = term[1:]

        if term not in self.encode:
            self.encode[term] = len(self.variables)

            # Random assignment
            self.variables.append(bool(random.getrandbits(1)))

        return self.encode[term]

    def write_solution(self, sol_filename):
        # Flip encode dictionary
        decode = {value: key for key, value in self.encode.items()}

        solution = open(sol_filename, "w")
        for i, variable in enumerate(self.variables):
            if variable:
                solution.write("{}\n".format(decode[i]))

        solution.close()
