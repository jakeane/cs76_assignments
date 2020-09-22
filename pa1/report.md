# PA1 Report

## Jack Keane

### Initial Discussion and Introduction

The upper bound for the number of states is `(# of chickens + 1) * (# of foxes + 1) * # of possible boat locations`, which for the basic case is `4 * 4 * 2 = 32`. For the first two factors, it is dependent on the number of chickens and foxes respectively. If there are `n` chickens, then a given state could have `0, 1,...,n` chickens, which is `n+1` possibilities. The same applies for foxes. As the boat can be either on the west or east bank, there are 2 possibilities.

#### Graph of initial first two rounds of states

![graph](pa1_states.png)

A requirement I have in order to take a 'step' between states is for the boat to cross the river. So, there are 5 possible ways to pick either 1 or 2 animals to cross the river (assuming there are enough chickens and foxes). Then in the next iteration of states, if there is only 1 animal on the east side of the river, then it must return in order to bring back the boat. If there are 2 animals, then either or both of them can return. Illegal states are colored red, and repeated states are colored orange (in this case it is just the root case).

### Code design

Is this part necessary?

### Building the model

In order to determine the successors in the `get_successors` method, I first consider the 5 possible traverses. Depending on the location of the boat, the traverse will add or subtract from the state (representing animals leaving/arriving to the west bank). Of course, this could create an illegal case, which is checked in the `is_safe` method. The two areas of 'illegality' is (a) more foxes than chickens, which violates the problem premise, and (b) invalid number of animals, such as <0 or >3 (if start_state is (3,3,1)) foxes/chickens at a bank.

### Breadth-first search

Not much to say here. Used a `set` to determine if state has already been visited, and used a `deque` to implement a queue. when the current node within the search as the goal node, then backchaining occurred, and its result was returned.