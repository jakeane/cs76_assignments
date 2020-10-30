# PA5: Logic README

## COSC 76 20F

## Jack Keane

### To Run

There are two main files for executing code: `solve_sudoku.py` and `MapColoring.py`. However, it is worth noting that if a `.cnf` file is the sole parameter for most solvers.

It is worth mentioning the my programs expect `.cnf` files to be in the `cnf/` directory and for `.sol` files to be in the `solutions/` directory. `.sud` files, however are expected to be in the main directory.

#### Solve Sudoku

There are three command line arguments here:

- The first is the `.sud` file.
- The second specifies the solver to use.
  - If the number is 1, then it will use the GSAT solving algorithm.
  - If 2, then the WalkSAT algorithm.
  - If otherwise, it will use DPLL.
- The last is a number 1 or 0. If the number is 1, then a full `.cnf` file is generated for the solver. If the numer is not 1, then the default `.cnf` file is generated.

#### Map Coloring

Here there is only one command line argument:

- An integer to specify which data to use.
  - If 0, then it will use the Australia problem
  - If 1, then the Petersen graph
  - If 2, the Canada providence problem
  - Otherwise, it will just exit
