# PA2: Mazeworld Report

## Jack Keane

### A-star Search

I changed how 'visited' nodes are tracked. Instead of having 'visited cost' be a dictionary within the search method, I had it be an instance variable inside of the node. It's value would be the sum of the parent node's visited cost and the transition cost. The visited cost of the root is 0.

Before diving into the key funcitonality of my A-star implementation, I will discuss the basic boilerplate. As opposed to BFS, the main difference is the queue we use, which is a priority queue now based on the A-star heuristic. The other difference is that we account for movement of the bot's. If they do not move, cost does not increase on the successing node.

Now, for the priority queue, we keep track of two variables, the priority queue itself, which is implemented as a heapified list, and a dictionary that maps visited states (note that they are not necessarily in the queue) to the node with the best heuristic cost. So, when a new state is added to the queue with `add_node()`, we check if the state has already been visited. If it has not, then it is put in the queue, but if it has been visited, then we check if it's heuristic cost is improved. If so, then the original state is marked as 'removed' and the new state is added to the queue.

To keep track of 'removed' states in the queue. The dictionary values are 2-element arrays, where the first element is the node itself, and the second is a boolean signifying if it has been removed. So, when an item is popped from the queue, we check if the signifier is true. If so, it is ignored and we pop the next item off the queue.

### Multi-robot coordination

First to discuss the program. For `get_successors()`, we first update the maze, so when `maze.has_robot()` is called later on, the maze is up to date. The other thing of note with in the successors method is that new 'states' are created by assembling multiple tuples together. The first is a single element tuple of the 'next robot to move', then the bot positions are spliced and the changed bot is placed in the gap.

Now for the questions:

1. The system can be represented a list of numbers, the first element signifies the robot that will try to move next, the following elements are the coordinates for the 1st, 2nd, ... , kth robot in that exact order.
2. The upper bound on the number of states in the system is `k * (n*n)^k`, where `k` is the number of bots, `n` is the width and height of the maze. If the maze is not a square shape, then `(n*n)` can be changed to `(n*m)`. This of course does not account for walls added or robots colliding.
3. There are roughly `k * (((n*n) - w)^k - \binom{((n*n) - w)^k}{k})` states that represent collisions. `((n*n) - w)^k` represents all possible orientations for the bots, and `\binom{((n*n) - w)^k}{k}` represents all the orientations that do not have any collisions. By finding the difference between the two, you get only the orientations that have collisions. This difference is then multiplied by `k` for each robot that is trying to move within the orientation.
4. No. The branching factor is 5, and the length of the solution scales with the dimensions of the board and the number of robots. This means the time/space complexity is `(kn)^5`, which does not scale well at all, so it is not computationally feasable. 
<br/><br/>
Due to my curiosity, let us assume that each robot has to travel to the opposing corner (or nearly as much), then each robot needs to travel `2n` squares. If there are few robots skipping turns, then there would be just above `k * 2n` moves in the solution. Each state has a branching factor of 5, so the time and space complexity are `(kn)^5`. As a very hasty calculation of the cost when `n = 100` and `k = 10`, we will calculate time at a lower scale and multiply. When `n = 6`, `k = 3`, and the robots start in separate corners and end in opposing corners, the program took 4.369 seconds. I then multiplied this value by `(1000/18)^5 = 529221494.013`, the ratio in complexity. This means that the extreme case would take *73 years* to complete.

5. Manhatten and Euclidian distance are good heuristic functions for this problem. *need to explain*
6. *do some tests*
7. *8-puzzle stuff*
8. *8-puzzle stuff*
