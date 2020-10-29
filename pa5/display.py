from Sudoku import Sudoku
import sys


def display_sudoku_solution(filename):

    test_sudoku = Sudoku(int(sys.argv[2]) == 1)
    test_sudoku.read_solution(filename)
    print(test_sudoku)


if __name__ == "__main__":
    display_sudoku_solution(sys.argv[1])
