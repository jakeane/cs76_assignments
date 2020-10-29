from Logic import Logic
import sys


class DPLL(Logic):
    def __init__(self, cnf_filename):
        super().__init__(cnf_filename)
        self.visits = 0

    def dpll_satisfiable(self):
        model = dict()
        return self.dpll(self.variables, model)

    def dpll(self, symbols, model):
        self.visits += 1
        print(len(model), self.visits)

        result = True
        for clause in self.clauses:
            status = self.dpll_clause_eval(model, clause)

            # If a clause in inconclusive
            if status == 0:
                result = False

            # Returns false if a clause is false in model
            elif status == -1:
                return False

        # Returns true if every clause is true in model
        if result:
            for symbol, value in model.items():
                self.variables[symbol] = value
            return True

        # Attempt pure symbol heuristic
        p, value = self.find_pure_symbol(symbols, model)
        if p is not None:
            symbols[p], model[p] = None, value
            return self.dpll(list(symbols), dict(model))

        # Attempt unit clause heuristic
        p, value = self.find_unit_clause(model)
        if p is not None:
            symbols[p], model[p] = None, value
            return self.dpll(list(symbols), dict(model))

        # Otherwise guess with first unassigned symbol
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

                    # If not seen before, initially assume pure
                    if variable not in purity:
                        purity[variable] = clause[variable]

                    # If seen again with different value, then not pure
                    elif purity[variable] != clause[variable]:
                        purity[variable] = None

        # Return first pure symbol if any
        for variable in purity:
            if purity[variable] is not None:
                return variable, purity[variable]

        return None, None

    def find_unit_clause(self, model):

        # Could use 'unsatisfied_clauses' like the pure symbol heuristic
        # However, satisfied clauses are filtered efficiently anyways
        for clause in self.clauses:
            # Assume not unit clause
            is_unit_clause = False
            symbol, value = None, None

            for variable in clause:
                if variable not in model:
                    # First unresolved variable means unit clause
                    # But second means not unit clause
                    if is_unit_clause:
                        is_unit_clause = False
                        break
                    else:
                        is_unit_clause = True
                        symbol, value = variable, clause[variable]

                # Clause satisfied, so can't be unit clause
                elif model[variable] == clause[variable]:
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

        # If all variables assigned at this point, the clause is false
        if clause_assigned:
            return -1
        else:
            return 0


if __name__ == "__main__":
    sat = DPLL(sys.argv[1])
    sat.dpll_satisfiable()
    print(sat.variables)
