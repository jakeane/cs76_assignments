# PA6: Hidden Markov Models Report

## Jack Keane

### Description

#### Implement Model and Filtering

The first aspect of this model is to move through the maze and collect a sequence of sensor readings, which was done with a for loop.

Then, we need to determine several condional statements:

- `P(e_i|X_i)` is determined for the entire maze by looking at the color of each tile and checking if it matches the scanned evidence. If so, then the probability that we assign the TPR to that location, and if not, then we assign the FPR divided by the size of the evidence domain minus one. We do this because we assume that if the scan was incorrect, then there is an equal probability to be any _other_ color.
- `P(X_i|x_{i-1})` is the transition model, so, for a given floor tile, I determine the adjacent tiles. If there are fewer adjacent tiles, then there are more walls for the robot to run into, causing it to stay in place. Given there are 4 directions of movement, I assign adjacent tiles 0.25 probability and the tile itself the remainder.
- `P(x_{i-1}|e_{0:i-1})` is simply the state of probabilites from the previous iteration, and they get multiplied elementwise with the transition model. The result is an array of representing the probabilities of entering a given tile. As we are doing filtering, we simply take the sum of the array.

After these are all calculated and multiplied together, the product becomes the new current state, and the process/calculations are repeated. At the end, we take a guess of the current position of the robot based on the highest probability.

#### Viterbi

To implement the Viterbi algorithm, some slight modifications had be made from the previous algorithm. My approach was to determine the most likely end state, and then backtrack to its most likely parent state until I reach the root. This was done with a list of matrices that represent the maze at each time step. The value in each tile is it's parent tile, so we simply had to iterate through the list in reverse, query a specific tile to generate a new tile, then carry on to the next iteration.

### Evaluation

#### Implement Model and Filtering

The filtering algorithm seems to do a good job at predicting the position of the robot. The mistakes it makes are quite reasonable. For example, if the robot is moving along the series of tiles with the same color, it is difficult to be exact with the position. This problem is compounded when it moves and scans a tile with a different color. Given the wide array of positions with moderate probability, there may likely be multiple adjacent tiles with the new color, so it is difficult to determine which is the correct tile.

Another interesting observation is when a bad color scan was made. Usually, it can 'recover' given enough timesteps afterwards. However, when the mis-scan's color is not adjacent to any probable position, it causes a drastic change in the probability distribution. Essentially the model is 'thinking' that an impossible move was just made, therefore there must be an error in one of the previous scans. For that reason, the robot could be in a wide range of locations, and we just need the following series of scans to converge on a set of possible positions.

I also tried this algorithm on some of my PA2 mazes. I noticed that the HMM can easily count out some tight spaces, which allows better accuracy. This is likely due to the limited sequences that can occur in tight spaces. Given enough evidence, the model can 'prove' that the observed sequence is not possible in a given tight space.

#### Viterbi

Similarly to the filtering algorithm, there can be issues when a robot moves along and scans a series of tiles with the same color. However, it seemed to guess the path with relatively okay accuracy.

One thing I wanted to see, however was when a bad scan was made. Would the model still predict the path correctly at that bad scan? It seemed that most of the time that was not the case in open mazes. However, in confined mazes, it was able to override the bad scan, which essentially says 'I know this was a bad scan due to the amount of supporting evidence'.
