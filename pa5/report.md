# PA5: Logic Report

## COSC 76 20F

## Jack Keane

### Description

#### General

To try out different algorithms, I created a base class, `Logic.py`, that initializes the problem and prints out solution files.

The problem is created from the `.cnf` file passed in through the parameters. With each clause that is read, each unique variable is encoded to an integer value 'id'. This integer value maps to an index in `self.variables`, a boolean array. The clauses are dictionaries where variable id's are mapped to the presence of a negation.

In order to improve runtime, I created an instance variable `self.domains`. This was a dictionary mapping variable id's to a list of clauses in which they were involved. In implementation of `SAT`, it allows much quicker scoring as the number clauses visited per variable is reduced by 98%.

#### GSAT

There is really only one key difference between GSAT and WalkSAT, so most of the description will occur here. That key difference is the list of variables from which we select from. GSAT selects from _all_ variables, and WalkSAT selects from a _clause_ that is unsatisfied. The other difference is the limit of iterations, where GSAT has 200,000 and WalkSAT has 100,000.

The structure of the algorithm is quite simple. It repeats a while loop until every clause is satisfied. Within the loop, we pick a variable from a list depending on the algorithm. There is a probability that a random variable is selected, but otherwise we go through a process of scoring each variable in the list.

To score, I iterate through the variables domain (see general) and count how many are satisfied. Then, I flip the variable and see how many are now satisfied, and finally I return the difference. This allows me to accurately keep track of the number of satisfied clauses without checking all of them.

After scoring each variable, I end up with a list of variables with the best score, from which I select randomly and flip. Then the next iteration starts.

#### WalkSAT

The implementation of WalkSAT is nearly identical, but I instead pass in a different method of generating a list of candidate variables, which randomly selecting an unsatisfied clause. Otherwise the process is quite identical.

#### DPLL

I also decided to implement the DPLL algorithm. It kind of feels like the backtracking algorithm from the CSP assignment. This makes sense as we are again trying to find a complete, consistent assignment of variables. This time though, the structure of information is different.

The different structure of information allows us to use different heuristics for selecting variables. The first heuristic, 'pure symbol', allows us to satisfy multiple clauses at once, where it iterates through all unsatisfied clauses and picks a variable whose literal is the same throughout. One way this could have been improved is by selecting the pure variable that was present in the most clauses. The other heuristic, 'unit clause', is kind of similar to deductive logic. It returns the first unsatisfied clause that only has one unresolved value, which means that value has essentially been deduced.

However, if none of the heuristics succeed, then we simply guess a value as true then false. Upon determining the variable and its respective values it enters a layer of recursion.

#### PL-Resolution

I also tried to implement the PL-resolution algorithm, but I was ultimately unsuccessful. I think I went wrong in the way I structured my knowledge base. It was difficult to do, as we did wanted to have unique values _and_ maintain constant time. I thought I could create a dictionary of dictionaries, where the key was a stringified version, but it does not account for the order in which variables are added into the dictionary.

Also, when I was trying to resolve two clauses, I really struggled in building an algorithm to produce the resolvants. It was difficult to handle multiple conflicts, but I think the algorithm is correct for the most part. I still feel like I am missing some edge cases through. Again, I think the structure of the knowledge base really undermined this.

Ultimately this is something I'll have to return to in the future.

#### Map Coloring

Converting the map coloring problems into CNF was quite easy. I followed the structure from the `Sudoku` module's CNF conversion. Fortunately, my algorithm implementations were generalized enough to allow this problem to work with any algorithm.

### Evaluation

#### GSAT

This algorithm does a good job converging to a 'near' solution, but it really struggles to get over the hump. It seems very dependent on the threshold for randomization, so it seems that GSAT would frequently find a local minima. Also, it required some optimization to have a reasonable runtime, as running through 3,000 clauses for 700 variables is not scalable.

#### WalkSAT

This algorithm did a much better job at getting a solution from a near solution state. Also it's runtime was much better as less variables were checked.

In comparision with GSAT, this algorithm is definitely preferable at scale, and at smaller scale, like the map coloring, there does not seem to be much of a difference. This is likely due to few local minima.

#### DPLL

One thing I quickly realized after testing this algorithm is that I needed to expand the `.cnf` files (see README). The default CNF for sudoku did not have negations by row, column, or block, meaning a specification that a value cannot show up multiple times in a row, column, or block. This lack of information essentially turned the DPLL algorithm into a backtracking DFS algorithm, which frequently got stuck at ~150 variables. This is because there is not enough information to deduce further, so it resorts to guessing.

By adding in additional negations, we are quickly able to find unit clauses. A single assignment seems to propogate across many, many other variables, and there is minimal guesswork. Within the 729 variables, there were only 760 visits roughly, which means very little guessing was needed.

In comparison to GSAT and WalkSAT, this algorithm is much better as it can deduce in a good manner, and maybe some of the heuristics could be implemented to a SAT algorithm.

#### Map Coloring

These problems worked well with the logic algorithms, but it is difficult to compare with CSP as they both solved quite quickly. I do believe CSP had less 'visits' but there was more work done behind the scenes for each visit.

### Discussion

#### WalkSAT

As mentioned in the extension, WalkSAT violates contraints at every step, even if the cell value is known beforehand. In my opinion, this is fine because I think escaping local minima is very important in this algorithm, and it can be hard to do so in a given situation. Being able to disregard known values could potentially provide an escape. On the other hand, being able to disregard known values could potentially lead to building a solution on a bad premise. It may cause the algorithm to rely on a random flip to correct a mistake on a known value, or it can even prevent a solution to be reached without restarting.

#### Ivor Spence

With the naive generation of CNF files with the modification specified in the DPLL section, redundancy was inevitable for Sudoku. However, I do not think redundancy is too helpful in this case for the SAT algorithms. I think it has to be a lot more deliberate. This means that the repeated clauses could be used to emphasize, like for known values or maybe some tough aspect of a given board.
