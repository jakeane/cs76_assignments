from Logic import Logic
from collections import deque


class PL(Logic):

    def __init__(self, cnf_filename):
        super().__init__(cnf_filename)

    def pl_solve(self):
        assigned = dict()
        unassigned = deque([i for i, variable in enumerate(self.variables)])

        # convert knowledge base into dict for easy lookup
        kb = {str(clause): clause for clause in self.clauses}

        while unassigned:
            variable = unassigned.popleft()

            # See if True can be assigned
            if self.pl_resolution(variable, False, assigned, kb):
                assigned[variable] = True

            # See if False can be assigned
            elif self.pl_resolution(variable, True, assigned, kb):
                assigned[variable] = False

            # If not enough info, then save for later
            else:
                unassigned.append(variable)

        # Assign symbols at end
        for symbol, value in assigned.items():
            self.variables[symbol] = value

    def pl_resolution(self, alpha, is_neg, assigned, kb):

        # convert assigned clauses into dict for lookup
        assigned_clauses = {str({var: value}): {var: value}
                            for var, value in assigned.items()}

        # combine assignments with kb
        clauses = {**kb, **assigned_clauses}

        # If already in kb, then no need to resolve
        if str({alpha: not is_neg}) in clauses:
            return False
        if str({alpha: is_neg}) in clauses:
            return True

        # at -alpha into kb
        clauses[str({alpha: is_neg})] = {alpha: is_neg}

        new = dict()
        checked = set()

        while True:
            for clause_i in clauses:
                for clause_j in clauses:
                    # ensure pair not yet visited
                    if clause_i != clause_j and (clause_j, clause_i) not in checked:
                        checked.add((clause_i, clause_j))

                        # resolve pair
                        resolvents = self.pl_resolve(
                            clauses[clause_i], clauses[clause_j])

                        # if empty clause found return
                        for resolvent in resolvents.values():
                            if len(resolvent) == 0:
                                return True

                        # merge in resolvents
                        new = {**new, **resolvents}

            new_loop = False
            for new_clause in new:
                # If new info found, merge and continue
                if new_clause not in clauses:
                    clauses = {**clauses, **new}
                    new_loop = True
                    break

            if new_loop:
                continue

            return False

    def pl_resolve(self, clause_i, clause_j):

        # Determine number of conflicts
        # If multiple conflicts, then multiple clauses can be derived
        conflicts = 0
        for var in clause_j:
            if var in clause_i:
                if clause_i[var] != clause_j[var]:
                    conflicts += 1

        if conflicts == 0:
            conflicts = 1

        resolvants = [dict() for _ in range(conflicts)]

        # 'None' refers to when a clause has both -X and X

        for var in clause_j:
            # If conflict
            if var in clause_i and clause_i[var] != clause_j[var]:

                conflicts -= 1

                # If one is clause has both, assign single to one resolvant
                if clause_i[var] is None:
                    resolvants[conflicts][var] = clause_j[var]
                elif clause_j[var] is None:
                    resolvants[conflicts][var] = clause_i[var]

                # Assign both to rest of resolvants
                for i in range(len(resolvants)):
                    if i != conflicts:
                        resolvants[i][var] = None

            # Otherwise just add in value from clause_j to all
            else:
                for i in range(len(resolvants)):
                    resolvants[i][var] = clause_j[var]

        # Get unseen values from clause_i
        for var in clause_i:
            if var not in clause_j:
                for i in range(len(resolvants)):
                    resolvants[i][var] = clause_i[var]

        return {str(resolvant): resolvant for resolvant in resolvants}
