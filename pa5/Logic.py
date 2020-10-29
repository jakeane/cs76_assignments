import random


class Logic:
    def __init__(self, cnf_filename, threshold=0.9):

        self.variables = []
        self.encode = dict()
        self.threshold = threshold
        self.read_cnf(cnf_filename)

        self.largest_model = 0
        self.visits = 0

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

    def write_solution(self, sol_filename):
        decode = {value: key for key, value in self.encode.items()}

        solution = open(sol_filename, "w")
        for i, variable in enumerate(self.variables):
            if variable:
                solution.write("{}\n".format(decode[i]))

        solution.close()
