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

5. Manhattan distance is a good heuristic function for this problem, where the sum of Manhattan distances of each robot to it's goal is the heuristic. Monotonic means that it's estimate to reach the goal is always less than or equal the estimate of its successor plus the distance to the successor. So, Manhatten distance is monotonic as any movement of a robot would increase cost by 1, and the lowest value that the heuristic would be decreased is 1, where the robot moves in (one of) the shortest path(s) to the goal. Therefore, the estimated cost, cost plus heuristic, will never get lower with any movement of the robot. For the same reason, Euclidian distance would also work, as the lowest value that the heuristic would be decreased is 1, where the robot is in the same row/column as its goal and it moves towards the goal.
6. The first test I created myself was a corridor problem, where the robots had to reverse order and head to the opposite end. An extra space was added on the side of the corridor to help. 
<br/><br/>
The next test I made was for a horseshoe-shaped map, where there is corridor to connecting the two sides. This forced the robots to idle while one robot traversed the map, and the robots behaved as intended.
<br/><br/>
The third test was more of a runtime test, where the maze was simply larger in size. However, it was quite jagged in shape, which makes heuristics less useful. Thus many more nodes were visited.
<br/><br/>
The last test was on a very large maze, 45 x 45, also with a jagged shape. This was just another limits test.

7. The 8-puzzle is a special case of this problem because there is only one open space in the board/maze, thus the movement of the tiles/robots is very restricted. The brings the Manhattan heuristic into question, as a tile/robot cannot move in an ideal path as there are other tiles/robots in the way, so the optimal path for a tile/robot may be longer than the ideal path in reality. Also moving a tile/robot into it's ideal location my displace other tiles/robots from their respective goal locations. I would argue that Manhattan heuristic is still good, but a modification is likely needed in order to account for the restrictive movement in the problem.
8. The two disjoint sets of 8-puzzle arrangements are those that are 'solvable' and those that are 'not solvable'. This can be determined at the beginning of the search, as to prevent a needless search on an unsolvable puzzle. In order to determine whether or not it is solvable, we first flatten the board with respect to the tiles, thus resulting in a list of numbers. Then we calculate the number of 'switches' between adjacent numbers required to sort the list in ascending order. If the number of switches is odd (such as [3,1,2,4,5,6,8,7] where three switches are required), then the puzzle is unsolvable. If it is even, then it is solvable.

#### Bonus

As an idea for how I would implement the bonus, where the robots can move simultaneously, the successors algorithm would be slightly different. First off, the state would remove the first variable, which is now irrelevant. Then, the successor function would loop through all 5 possible moves for each of the robots. As long as the set of movements are valid, the new state would be added.

### Blind Robot with Pacman Physics

As mentioned in the problem, the initial state is all open positions in the maze. This is done by iterating all spaces in the maze and checking if it is a floor or not. As opposed to the previous problem, we do not consider `(0, 0)` to be a move as it would not change the state.

As for `get_successors()`, we iterate through each of the moves through last time, then we apply that move to each of the potential positions. If the new position is not floor, that means the robot would stay in place. After determining the new position, it is added into a set in order to prevent repeats.

From here, we needed a heuristic to estimate the number of moves needed to attain a solution. The best of which I wrote was called `compact`, which collected the max and min of the coordinates of the potential states. This would essentially provide the 'width - 1' and 'height - 1' of the smallest rectangle that could encompass all positions. The sum of these two values represent the best case number of moves to reach the goal state, which is within an open space against two adjacent walls. Say the walls were on the south and west sides, then you would attempt to move the robot south 'height - 1' times and then west 'width - 1' times. This is an underestimate as there could be obstacles or lack of walls to allow this, thus making it admissable. This was the best performing heuristic I found.

The next heuristic I wrote was called `colrow`, which behaves similarly to `compact`, it's value is calculated by finding the number of unique row and column values within the coordinates. This would result in a value that is always less than or equal to `compact`. This is because the coordinates could be split into two separate groups, and in theory, this could allow groups of coordinates to compact itself separately before merging together. However, when the potential coordinates becomes sparse, the heuristic becomes less effective. At such a point, you could switch heuristics to approach a solution faster.

There were also some bad heuristics I wrote. They were either not admissable, or their values were extreme underestimates, thus causing many more nodes to expand. The first was called `isolated`, and it's value was the number of isolated positions on the maze. This was an attempt to discourage positions from spreading out and isolating, and instead encourage positions to stay together. However, this heuristic vastly underestimates, so it is not very useful in any case.

Another bad heuristic was the first one I wrote, one that many others probably wrote, `first`. It's value was simply the number of possible states. Contrary to my initial thoughts, this heuristic is not admissable. As proof, consider a 2x2 maze filled with potential states. It would take 2 moves to solve, but the heuristic would return 4.

Another bad heuristic was an extension of the previous, `log2`. It took the value from `first` and calculated the 'log2' of it. In early situations, this heuristic would vastly underestimate, so the search would branch out a lot at the beginning. Not ideal.

The last bad heuristic I'll mention is the `further_points` which follows similar thinking to the `compact`. It simply found the furthest apart coordinates in the state, and returned their Manhattan distance. As these points were furthest apart and they needed to come together in some way, it seemed like a worthwhile value to find. However, this one did not seem to work.

As for heuristics to consider, not create. I think a heuristic that could first look at the current state or the position of each pair of coordinates before making a calculation would be more optimal. This, in theory, would allow the agent to select a heuristic that best estimates the distance from solution dependent on the state. It could probably handle obsure or difficult cases well. Essentially, it's an ensemble of heuristics with a 'decision-maker' to select the correct one.

In the picture below is a series of states. The red line signifies few states being skipped. At the beginning, the movements are mostly towards northwest in order to get the left hand positions out of the coridor while simultaneously removing values from the right hand side. Then after clearing the coridor (red line), the movement is focused towards northeast as the states are either lined up at the top or are lingering just below.

![states](sensorless_states.png)