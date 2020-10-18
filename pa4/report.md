# PA4: Constraint Satisfaction Problem Report

## COSC 76 20F 

## Jack Keane

### Description

#### CSP Program

For the data management of this program, I had 3 main variables and 3 accessory variables. The main variables were not constructed in the root object as to account for the variety of implementations of CSP. The child objects were responsible for constructing the main variables. The first of the main variables, `self.variables`, was a 'graph' of the variables implemented in a dictionary, where edges signified constraints. The next main variable, `self.domains`, was a dictionary mapping variables to their respective domain of values. The last main variable, `self.constraints`, was a set of edges that signified the binary constraints. As for the accessory variables, they pertained to the adjustable aspects of the algorithms such as AC-3 inference, variable selection, and value sorting.

Generally speaking, I followed the pseudo-code provided in the textbook. The top level method, `backtracking_search()` simply calls the recursive method, `backtrack()` as well as prints the output. The ways that `backtrack()` differs from the textbook pseudo-code start with the options (see accessory variables above) to select the variable and sort the domain values, both methods of which are specified by the user. The next bit of difference is the `changelog`, which is specified in a very general sense in the pseudo-code. It is initialized as a dictionary that maps variables to a set where removed values are specified. Next, to allow the option for inference, I created a odd looking `if` statement. If there is `infer` is true, it will then call `ac3()` to create inferences. If `ac3()` detects a failure, the `if` statement will be false, and the assignment is immediately reverted. In all other cases, the `if` statement is true, where inside it will enter a layer of recursion and return successful results. After unsuccessful recursion, the assignment and changes are reverted via `changelog`.

#### Heuristics

The 'minimum remaining values' heuristic was quite trivial to implement, as we just needed to iterate through unassigned variables and return the one with the smallest domain.

The 'degree' heuristic was interesting however. I initially thought it was a simple 'number of unassigned neighbors', but it is actually dependent on the problem. For the map coloring, that is the case. However, for the circuit board problem, something different is needed. In order to infer how 'constraining' a variable was, I used the area of the component (width * height) as they are well correlated. I thought about manually calculating how many positions a variable had between each of its neighbors, but that would not scale.

The 'least constraining value' heuristic was more simple however, given I had a way to define an illegal assignment between two variables, I could incorporate that into the heuristic. Thus this needed to be adapted to the problem.

#### Inference

The `ac3()` and `revise()` methods were quite directly implemented from the pseudo-code aside from one thing. As each constraint was directed in each way (like a -> b and b -> a), the for loops needed to be done for each value in a binary constraint, whereas in the pseudo-code it was just for one value.

#### Map Coloring

For the map coloring problem, I directly passed into the constructor a graph of the variables and their respective neighbors. The domain for each variable was the exact same list passed in by the user.

Degree was defined by the number of unassigned neighbors, and the 'constraint' was that neighbors could not have equal values, this is relevant for the `check_consistent()`, `constraint_unsatisiable()`, and `constraint_helper()` functions defined in the root object.

Testing is decribed in the 'evaluation' section.

#### Circuit board layout

For the circuit board layout problem, I passed into the constructor a list of the variables and the size of the board. The `self.variables` object could be inferred from there, as every variable was 'neighbors' with the other variables. The `self.domains` could be inferred from the size of the component and board. The helper function `can_fit()` was used to determine if a component would fit in a certain position of an empty board. `self.constraints` was defined as every possible pair of variables.

Degree of a component/variable was determined by it's size. As mentioned above, I could have calculated exactly how many positions a given component had influence over, but that would not scale well. The size of the component correlates well and is constant time.

The 'constraint' was defined as no overlap between two components, which required comparing the left/right most point and right/left most point as well as the top/bottom most and the bottom/top most point between two components.

### Evaluation

#### CSP Program

The program works quite well as it follows the pseudo-code quite directly. However, I had some issues with maintaining the changelog. Initially the address of the domain and changelog of a given variable was the same, which led to unexpected outcomes. Otherwise, not much interesting stuff to evaluate here.

#### Heuristics

While the book says that MRV is the preferable heuristic, which I agree with, it seemed to me that the degree heuristic was preferable when there was no solution. Across both problems types, less nodes were visited when the degree heuristic was used instead of MRV. However, it seems that MRV is preferable for successful solutions, so I would argue the preferable heuristic depends on the predicted solvability of the problem. If it is unlikely to solve, degree heuristic would be the best way to determine that. Otherwise, use MRV.

A thing to note between MRV and degree is that I could have implemented a tie-breaker for MRV as the degree heuristic, but it seemed trivial for the scale of problems we were tackling.

A last note is that while LCV seemed trivial for the circuit-board problem, that was likely because when LCV was *not* implemented, it would pick the first value in the domain list, which would usually hug up against the boundary or other components.

#### Inference

Inference was great for detecting early failures. In some tests, where I only provided two colors for the map coloring problem, it only visited one node as the constraint propogation was able to infer empty domains quickly. It also generally was able to reduce the number of visited nodes, drastically in failures, but I was unable to develop a test that reduced the number of visited nodes with inference on a successful problem. I assume there are some cases that cause that.

#### Map Coloring

This problem seems to run in linear time relative to the number of variables, which is likely due the low number of constaints. It seems that most of the domains are 'solved' before they are 'assigned'.

#### Circuit Board Layout

This problem does not run in linear time, as bad value selection is actually influential, but this displayed the backtracing ability of the CSP algorithm. When a component was badly placed, inference would sometimes prevent it from entering recursion. If inference was not involved, it was able to display failure and backtracking.

### Discussion

As mentioned earlier regarding the `can_fit()` helper function, the domain of a given component was determined by positions where the entire component fit on the board. This was done by comparing the sum of the x/y position and size to the respective board dimension.

The constraint is mentioned above in the description. The legal pairs are `[(0, 0), (3, 0)], [(0, 0), (3, 1)], [(0, 0), (4, 0)], [(0, 0), (4, 1)], [(0, 0), (5, 0)], [(0, 0), (5, 1)], [(0, 1), (3, 0)], [(0, 1), (3, 1)], [(0, 1), (4, 0)], [(0, 1), (4, 1)], [(0, 1), (5, 0)], [(0, 1), (5, 1)], [(1, 0), (4, 0)], [(1, 0), (4, 1)], [(1, 0), (5, 0)], [(1, 0), (5, 1)], [(1, 1), (4, 0)], [(1, 1), (4, 1)], [(1, 1), (5, 0)], [(1, 1), (5, 1)], [(2, 0), (5, 0)], [(2, 0), (5, 1)], [(2, 1), (5, 0)], [(2, 1), (5, 1)], [(5, 0), (0, 0)], [(5, 0), (0, 1)], [(5, 1), (0, 0)], [(5, 1), (0, 1)], [(6, 0), (0, 0)], [(6, 0), (0, 1)], [(6, 0), (1, 0)], [(6, 0), (1, 1)], [(6, 1), (0, 0)], [(6, 1), (0, 1)], [(6, 1), (1, 0)], [(6, 1), (1, 1)], [(7, 0), (0, 0)], [(7, 0), (0, 1)], [(7, 0), (1, 0)], [(7, 0), (1, 1)], [(7, 0), (2, 0)], [(7, 0), (2, 1)], [(7, 1), (0, 0)], [(7, 1), (0, 1)], [(7, 1), (1, 0)], [(7, 1), (1, 1)], [(7, 1), (2, 0)], [(7, 1), (2, 1)]`.

It doesn't convert to integers?

