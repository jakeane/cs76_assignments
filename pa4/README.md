# PA4: Constraint Satisfaction Problem README

## COSC 76 20F 

## Jack Keane

### Map Coloring

To provide problems to the solver, specify two variables: (1) A graph of regions implemented as a dictionary where the value is a list of neighbors, and (2) a list of colors. The other problem configs are trivial.

To solve, call `MapColoringCSP.backtracking_search()`.

### Circuit Board

To provide problems to the solver, specify two variables: (1) A list of tuples that represent the size of each component, and (2) the size of the board itself. The other problm configs are trivial.

To solve, call `CircuitBoardCSP.backtracking_search()`.