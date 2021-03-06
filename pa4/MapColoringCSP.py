from ConstraintSatisfactionProblem import ConstraintSatisfactionProblem


class MapColoringCSP(ConstraintSatisfactionProblem):

    def __init__(self, variables, values, infer=False, var_select=0, sort_values=False):
        super().__init__(variables, values, infer, var_select, sort_values)

        var_id = 0
        for variable in variables:
            # create mapping if needed
            if variable not in self.var_conv:
                self.var_conv[variable] = var_id
                var_id += 1

            neighbors = []
            for neighbor in variables[variable]:
                # create mapping if needed
                if neighbor not in self.var_conv:
                    self.var_conv[neighbor] = var_id
                    var_id += 1

                neighbors.append(self.var_conv[neighbor])

            # create translated pairing
            self.variables[self.var_conv[variable]] = neighbors

        for dom_id, value in enumerate(values):
            self.dom_conv[dom_id] = value

        # domains are assumed to be the same across variables
        self.domains = {variable: [i for i in range(
            len(values))] for variable in self.variables}

        # build list of edges/constraints
        for variable in self.variables:
            for neighbor in self.variables[variable]:
                # note that reversed tuple in condition prevents duplicates
                if (neighbor, variable) not in self.constraints:
                    self.constraints.add((variable, neighbor))

        # flip variable conversion to allow int to data translation
        self.var_conv = {id: var for var, id in self.var_conv.items()}

    # degree determined by number of unassigned neighbors
    def get_degree(self, variable, assignments):
        degree = 0
        for neighbor in self.variables[variable]:
            if neighbor not in assignments:
                degree += 1
        return degree

    # values of adjacent variables must be different
    def constraint_helper(self, var_a, var_b, val_a, val_b):
        return val_a == val_b


if __name__ == "__main__":

    map_data = {
        # Australia
        "aus": {
            "WA": ["SA", "NT"],
            "Q": ["SA", "NT", "NSW"],
            "T": [],
            "V": ["SA", "NSW"],
            "SA": ["V", "NT", "NSW", "WA", "Q"],
            "NT": ["SA", "WA", "Q"],
            "NSW": ["V", "SA", "Q"]
        },
        # Petersen graph
        "pete": {
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
        },
        # Canada
        "can": {
            "AB": ["BC", "NT", "SK"],
            "BC": ["AB", "NT", "YT"],
            "MB": ["NU", "ON", "SK"],
            "NB": ["NS", "QC"],
            "NL": ["QC"],
            "NS": ["NB"],
            "NT": ["AB", "BC", "NU", "SK", "YT"],
            "NU": ["NT", "MB"],
            "ON": ["MB", "QC"],
            "PE": [],
            "QC": ["NB", "NL", "ON"],
            "SK": ["AB", "NT", "MB"],
            "YT": ["BC", "NT"]
        }
    }

    colors = ["Red", "Green", "Blue"]

    map_problem = MapColoringCSP(
        map_data["can"], colors, infer=True, var_select=2, sort_values=True)

    # print(map_problem)
    # print(map_problem.mrv_heuristic({}))
    # print(map_problem.degree_heuristic({}))
    # print(map_problem.lcv_heuristic("I"))

    map_problem.backtracking_search()
