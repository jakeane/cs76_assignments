from DPLL import DPLL
from SAT import SAT
import sys
import os


def map_to_cnf(cnf_filename, data, colors):
    if not os.path.exists("cnfs"):
        os.makedirs("cnfs")

    file = open("cnfs/{}".format(cnf_filename), "w")
    for variable in data:
        clause = ""
        for color in colors:
            clause += map_literal(variable, color)
        clause += "\n"
        for i in range(len(colors)):
            for j in range(i+1, len(colors)):
                clause += map_literal(variable, colors[i], neg=True)
                clause += map_literal(variable, colors[j], neg=True)
                clause += "\n"

        file.write(clause)

    # build list of edges/constraints
    constraints = set()
    for variable in data:
        for neighbor in data[variable]:
            # note that reversed tuple in condition prevents duplicates
            if (neighbor, variable) not in constraints:
                constraints.add((variable, neighbor))

    for constraint in constraints:
        for color in colors:
            clause = ""
            clause += map_literal(constraint[0], color, neg=True)
            clause += map_literal(constraint[1], color, neg=True)
            clause += "\n"
            file.write(clause)

    file.close()


def map_literal(variable, value, neg=False):
    return ("-" if neg else "") + "{}_{} ".format(variable, value)


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

    # generate cnf
    options = ["aus", "pete", "can"]

    arg = int(sys.argv[1])
    if arg >= 0 and arg <= 2:
        select = options[arg]
        sol_filename = "{}_sat.sol".format(select)
        cnf_filename = "{}_sat.cnf".format(select)

        map_to_cnf(cnf_filename, map_data[select], colors)

        sat = SAT(cnf_filename)

        result = sat.gsat()

        if result:
            sat.write_solution(sol_filename)
