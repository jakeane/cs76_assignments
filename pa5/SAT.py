from display import display_sudoku_solution
import random
from collections import deque
import sys


class SAT:

    ############# PROBLEM INIT #############

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

    ############# PL Resolution #############

    def pl_solve(self):
        assigned = dict()
        unassigned = deque([i for i, variable in enumerate(self.variables)])

        kb = {str(clause): clause for clause in self.clauses}

        while unassigned:
            variable = unassigned.popleft()
            # print(len(unassigned), variable)

            if self.pl_resolution(variable, False, assigned, kb):
                print(variable, True)
                assigned[variable] = True
            elif self.pl_resolution(variable, True, assigned, kb):
                print(variable, False)
                assigned[variable] = False

            else:
                unassigned.append(variable)

        for symbol, value in assigned.items():
            self.variables[symbol] = value
        print(assigned)
        print(self.encode)

    def pl_resolution(self, alpha, is_neg, assigned, kb):

        assigned_clauses = {str({var: value}): {var: value}
                            for var, value in assigned.items()}

        clauses = {**kb, **assigned_clauses}

        if str({alpha: not is_neg}) in clauses:
            return False
        if str({alpha: is_neg}) in clauses:
            return True

        clauses[str({alpha: is_neg})] = {alpha: is_neg}

        new = dict()

        checked = set()

        while True:
            for clause_i in clauses:
                for clause_j in clauses:
                    if clause_i != clause_j and (clause_j, clause_i) not in checked:
                        checked.add((clause_i, clause_j))

                        resolvents = self.pl_resolve(
                            clauses[clause_i], clauses[clause_j])

                        for resolvent in resolvents.values():
                            if len(resolvent) == 0:
                                # print(clause_i, clause_j)
                                return True

                        new = {**new, **resolvents}

            new_loop = False
            for new_clause in new:
                if new_clause not in clauses:
                    clauses = {**clauses, **new}
                    print(clauses)
                    new_loop = True
                    break
            if new_loop:
                continue

            return False

    def pl_resolve(self, clause_i, clause_j):
        # resolvants = dict(clause_i)
        can_combine = True

        conflicts = 0
        for var in clause_j:
            if var in clause_i:
                if clause_i[var] != clause_j[var]:
                    conflicts += 1
        print(conflicts)

        if conflicts == 0:
            conflicts = 1

        resolvants = [dict() for _ in range(conflicts)]

        for var in clause_j:
            if var in clause_i:
                if clause_i[var] != clause_j[var]:
                    conflicts -= 1

                    if clause_i[var] is None:
                        resolvants[conflicts][var] = clause_j[var]
                    elif clause_j[var] is None:
                        resolvants[conflicts][var] = clause_i[var]

                    for i in range(len(resolvants)):
                        if i != conflicts:
                            resolvants[i][var] = None
                else:
                    for i in range(len(resolvants)):
                        resolvants[i][var] = clause_j[var]
            else:
                for i in range(len(resolvants)):
                    resolvants[i][var] = clause_j[var]

        for var in clause_i:
            if var not in clause_j:
                for i in range(len(resolvants)):
                    resolvants[i][var] = clause_i[var]

        return {str(resolvant): resolvant for resolvant in resolvants}

    ############# GSAT and WALKSAT #############

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

    ############# DPLL #############

    def dpll_satisfiable(self):
        self.model = dict()
        return self.dpll(self.variables, self.model)

    def dpll(self, symbols, model):
        self.visits += 1
        if len(model) > self.largest_model:
            print(len(model), self.visits)
            self.largest_model = len(model)

        result = True
        for clause in self.clauses:
            status = self.dpll_clause_eval(model, clause)
            if status == 0:
                result = False
            elif status == -1:
                return False
        if result:
            for symbol, value in model.items():
                self.variables[symbol] = value
            return True

        p, value = self.find_pure_symbol(symbols, model)

        if p is not None:
            symbols[p], model[p] = None, value
            return self.dpll(list(symbols), dict(model))

        p, value = self.find_unit_clause(model)

        if p is not None:
            symbols[p], model[p] = None, value
            return self.dpll(list(symbols), dict(model))

        p = self.get_first_symbol(symbols)

        symbols[p], model[p] = None, True
        recurse = self.dpll(list(symbols), dict(model))
        if recurse:
            return recurse
        else:
            model[p] = False
            return self.dpll(list(symbols), dict(model))

    def find_pure_symbol(self, symbols, model):
        unsatisfied_clauses = [clause
                               for clause in self.clauses
                               if self.dpll_clause_eval(model, clause) != 1]

        purity = dict()

        for clause in unsatisfied_clauses:
            for variable in clause:
                if variable not in model:
                    if variable not in purity:
                        purity[variable] = clause[variable]
                    else:
                        if purity[variable] != clause[variable]:
                            purity[variable] = None

        for variable in purity:
            if purity[variable] is not None:
                return variable, purity[variable]

        return None, None

    def find_unit_clause(self, model):

        for clause in self.clauses:
            is_unit_clause = False
            symbol, value = None, None

            for variable in clause:
                if variable not in model:
                    if is_unit_clause:
                        is_unit_clause = False
                        break
                    else:
                        is_unit_clause = True
                        symbol, value = variable, clause[variable]

                else:
                    if model[variable] == clause[variable]:
                        is_unit_clause = False
                        break

            if is_unit_clause:
                return symbol, value

        return None, None

    def get_first_symbol(self, symbols):
        for i, symbol in enumerate(symbols):
            if symbol is not None:
                return i

        # This probably won't occur
        print("WHAAA")
        return 0

    def dpll_clause_eval(self, model, clause):
        clause_assigned = True
        for variable in clause:
            if variable in model:
                if model[variable] == clause[variable]:
                    return 1
            else:
                clause_assigned = False
        if clause_assigned:
            return -1
        else:
            return 0


if __name__ == "__main__":
    sat = SAT(sys.argv[1])
    sat.dpll_satisfiable()
    print(sat.variables)

    # clauses = [{1: True, 2: True, 3: True}, {1: False, 2: False}]
    # assigned = {1: True, 3: False}
    # alpha = {1: False}
    # combined = clauses + [alpha]
    # final = {str(clause): clause for clause in combined}

    # additional = [{var: value}
    #               for var, value in assigned.items()]
    # addi = {str(clause): clause for clause in additional}

    # final = {**final, **addi}

    # print(final)
    # print({str({var: value}): {var: value} for var, value in assigned.items()})
