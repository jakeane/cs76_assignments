from DPLL import DPLL
from Sudoku import Sudoku
from display import display_sudoku_solution
import random
import sys
from SAT import SAT

if __name__ == "__main__":
    # for testing, always initialize the pseudorandom number generator to output the same sequence
    #  of values:
    random.seed(1)

    sudoku_problem = Sudoku(int(sys.argv[2]) == 1)
    sudoku_problem.load(sys.argv[1])

    puzzle_name = str(sys.argv[1][:-4])
    cnf_filename = "{}.cnf".format(puzzle_name)
    sol_filename = puzzle_name + ".sol"

    sudoku_problem.generate_cnf(cnf_filename)

    sat = DPLL(cnf_filename)

    result = sat.dpll_satisfiable()

    if result:
        sat.write_solution(sol_filename)
        display_sudoku_solution(sol_filename)
