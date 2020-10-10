# PA3: Chess Report

## COSC 76 20F

## Jack Keane

### Description

#### Minimax and Cutoff Test

The functions I wrote for the Minimax agent follow quite closely to pseudo-code the textbook. Within the main function `choose_move()`, I iterate through every possible move and append the `min_value()` to a list. However, when picking a move, it is important to acknowledge that mulitple moves may have the 'max value'. In order to account for that, I shuffle the list of legal moves before iterating through them. Then I simply pick the first move whose value matches the best value.

The `min_value()` and `max_value()` functions are quite close to the pseudo-code. The one note is that every iteration starts with incrementing a counter.

As for the cutoff test, this passes if maximum depth has been reached or when the board state is 'game over'.

#### Evaluation Function

As for the evaluation, I first check if the game is over. If so, I then check if the game is a stalemate, for which I return 0 as it is a tie. If it is not a stalemate, then we check if there is a checkmate (which I believe is the only other alternative). I assign 200 or -200 depending on the winner. Then, in order to motivate the AI to close out the game, I added a reward that increased when the checkmate was at a shallower depth. However, this sum is not yet returned. I evaluate the board state afterwards, as this will encourage the AI to aim for a 'better' win, where they maintain/promote their pieces and remove their opponents.

For general evaluation, I use the recommended material variant (pawn=1, knight=3, bishop=3, rook=5, queen=9, king=200). To implement I take a tally of all the pieces by type, and then I calculate the difference between white and black. These differences are then individually multiplied depending on the piece values, and then the sum its taken. That sum is the evaluation of the board state. If it is positive, it favors white, and it favors black if otherwise. To account for this, I check if the agent is playing white or black, and then adjust the evaluation accordingly.

#### Alpha-Beta Pruning

I wrote three different versions of this 'agent'. Each of which has different levels of optimization.

The first was the basic alpha-beta pruning algorithm, located in `NonOptAlphaBeta.py`, that generally follows the pseudo-code from the textbook. One thing I learned while implementing this algorithm is that it simply returns the best *value*, not the best *move*. After a new best move is found, the lower bound gets set to that value. So, if that value is found one depth below, it will be returned. This results in multiple occurence of the best value, although many of them are not factual. In order to account for this, the selected move from `alphabeta` is the *first* occurrence of the best value, similar to `minimax()`. However, it is much more important this time around, as it prevent suboptimal decision making. This also applied to subsequent iterations of this algorithm.

The next algorithm I wrote included a basic version of 'move-sorting', `SortAlphaBeta.py`, with the intention of 'pruning' more of the search tree. So, before iterating through the legal moves in min/max_value, they were sorted with a custom comparator, which used the evaluation function as the sorting value. I did not apply this sorting at the top level because I still wanted an element of randomness when selecting moves.

The last algortihm I wrote also used a transposition table, `AlphaBeta.py`, which saves the evaluation of a board state at a given depth. This table was leveraged in two ways. First, the comparator from `SortAlphaBeta.py` was modified to first query the table to check if the board state exists. If so, then it's respective value was returned. If not, then the evaluation function was performed on the board. It would have been better to prioritize boards that already existed in the table, as that would prevent needless searching in the case that on of those boards can cause a pruning event. The next place it is leveraged is while iterating through potential moves. If the resulting board state exists in the table, then no searching is needed, and its respective value is accessed and proceeds through the loop iteration.

Comparisons between these agents will be in the evaluation section.

#### Iterative Deepening

For the iterative deepinging, I made the iterations dependent on time. Meaning that I set a time limit on how long the AI is allowed to consider potential moves. This time limit is enforced within the same `if` statement that prunes the search tree. This allows the algorithm to return to the `main` level as quickly as possible and return the best found move.

It is important to note that it will not consider moves at the depth where the time limit gets enforced. This is for two reason. First is that the search tree was only partially searched, even when accounting for pruning. Therefore, the "best move" is likely not optimal. Second, the evaluation is relative, and whoever last moved is impactful to the resulting evaluation. One move could mean capturing a piece, which swings the evaluation in favor of the most recent person. This means that evaluations between depths are difficult to compare.

Another thing to note is that I used the `SortAlphaBetaAI.py` agent for the iterative model. This was because it is generally the fastest among the 'alpha-beta' varients.

### Evaluation

#### Minimax and Cutoff Test

Minimax is usable as long as the depth does not surpass 2. This is likely because there are roughly 27000+ nodes to calculate for any given move, so it takes a long time to view them all.

#### Evaluation Function

In order to improve this evaluation, I think we could consider non-material factors such as board positioning. What positioning exactly? IDK I'm not a chess expert. Regardless, the shortcomings in the evaluation are evident when an AI is attempting to close out a game. It will put the opponent into check, but it does not exactly try to 'corner' the opponent. During uneventful games, the AI will perform arbitrary moves that do not progress the game any further. I think this is due to the lack of foresight, so any move is equally unimpactful. Also, it's initial board development is quite erratic, which puts itself into inconvenient positions later in the game. 

However, the impact of depth is certainly noticable. At shallower depths, the AI clearly does not understand the repercussions of their actions as it is simply trying to capture other pieces at high risk.

#### Alpha-Beta Pruning

Between the three variants I wrote, there was an interesting balance between time and optimization. I measured the time by starting and ending a timer at the start and end of the top level function call. This measured the execution time of that function, and it was accumulated over the course of the game. The optimazation was measured by counting each instance of `max_value()` and `min_value()` over the course of the game.

I initially thought that the fully optimized variant, `AlphaBetaAI.py`, would perform the best across the board. Although it generally visited the fewest nodes, it was actually worse in terms of run time. It seems that the sorting and querying of the dictionary offset the benefits with respect to time. It turns out that the simple sorting variant, `SortAlphaBetaAI.py`, was the quickest, and it only slightly worse than `AlphaBetaAI.py` in terms of nodes visited. As for the non-optimized variant, `NonOptAlphaBetaAI.py`, it visited many many more nodes, but it's run time was slightly worse than `SortAlphaBetaAI.py`. These findings were somewhat surprising, but I think the correct response to this is to seek more optimization methods, that of which I will not attempt.

#### Iterative deepening

I kept a generally low time limit for the iterative deepening, roughly 5-10 seconds. The most common depth at this setting was 3. It would usually reach depth 3 quite quickly, so it was really hung up on depth 4. It seems that depth 4 is not ideal for short term settings. However, it was interesting to see how the depth would vary in certain situations. At the beginning and the end of the game, depth 4 was occasionally reached, but for most of the mid game, depths 2 and 3 were most common.

It seemed intuitive to maintain the values of previous board states over the course of multiple iterations. However, I think it removes optimality. The values saved at depth `i` do not always account for values at `i+1...inf`. Therefore, it seems to be detrimental to maintain previous values.

