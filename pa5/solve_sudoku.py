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

    sudoku_problem = Sudoku(int(sys.argv[3]) == 1)
    sudoku_problem.load(sys.argv[1])

    puzzle_name = str(sys.argv[1][:-4])
    cnf_filename = "cnfs/{}.cnf".format(puzzle_name)
    sol_filename = puzzle_name + ".sol"

    sudoku_problem.generate_cnf(cnf_filename)

    if int(sys.argv[2]) == 1:
        solver = SAT(cnf_filename)
        result = solver.gsat()
    elif int(sys.argv[2]) == 2:
        solver = SAT(cnf_filename)
        result = solver.walksat()
    else:
        solver = DPLL(cnf_filename)
        result = solver.dpll_satisfiable()

    if result:
        solver.write_solution(sol_filename)
        display_sudoku_solution(sol_filename)
