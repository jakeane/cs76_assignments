# PA3: Chess

## COSC 76 20F

## Jack Keane

### Description

#### Minimax and Cutoff Test

The functions I wrote for the Minimax agent follow quite closely to pseudo-code the textbook. Within the main function `choose_move()`, I iterate through every possible move and append the `min_value()` to a list. However, when picking a move, it is important to acknowledge that mulitple moves may have the 'max value'. In order to account for that, I shuffle the list of legal moves before iterating through them. Then I simply pick the first move whose value matches the best value.

The `min_value()` and `max_value()` functions are quite close to the pseudo-code. The one note is that every iteration starts with incrementing a counter.

As for the cutoff test, this passes if maximum depth has been reached or when the board state is 'game over'.

#### Evaluation Function

As for the evaluation, I first check if the game is over. If so, I then check if the game is a stalemate, for which I return 0 as it is a tie. If it is not a stalemate, then we check if there is a checkmate (which I believe is the only other alternative). I assign 300 or -300 depending on the winner. However, that value is not yet returned. I evaluate the board state afterwards, as this will encourage the AI to aim for a 'better' win, where they maintain/promote their pieces and remove their opponents.

For general evaluation, I use the recommended material variant (pawn=1, knight=3, bishop=3, rook=5, queen=9, king=200). To implement I take a tally of all the pieces by type, and then I calculate the difference between white and black. These differences are then individually multiplied depending on the piece values, and then the sum its taken. That sum is the evaluation of the board state. If it is positive, it favors white, and it favors black if otherwise. To account for this, I check if the agent is playing white or black, and then adjust the evaluation accordingly.

#### Alpha-Beta Pruning

A lot of the implementation is an extension of the previous `minimax()` and pseudo-code from the textbook, so I will bear you from those details. One thing I learned while implementing this algorithm is that it simply returns the best *value*, not the best *move*. After a new best move is found, the lower bound gets set to that value. So, if that value is found one depth below, it will be returned. This results in multiple occurence of the best value, although many of them are not factual. In order to account for this, the selected move from `alphabeta` is the *first* occurrence of the best value, similar to `minimax()`. However, it is much more important this time around, as it prevent suboptimal decision making.

#### Iterative Deepening

Need to double check if this implementation is correct.

### Evaluation

#### Minimax and Cutoff Test

Minimax is usable as long as the depth does not surpass 2. This is likely because there are roughly 27000+ nodes to calculate for any given move, so it takes a long time to view them all.

#### Evaluation Function

In order to improve this evaluation, I think we could consider non-material factors such as board positioning. What positioning exactly? IDK I'm not a chess expert. Regardless, the shortcomings in the evaluation are evident when an AI is attempting to close out a game. It will put the opponent into check, but it does not exactly try to 'corner' the opponent. During uneventful games, the AI will perform arbitrary moves that do not progress the game any further. I think this is due to the lack of foresight, so any move is equally unimpactful. Also, it's initial board development is quite erratic, which puts itself into inconvenient positions later in the game. 

However, the impact of depth is certainly noticable. At shallower depths, the AI clearly does not understand the repercussions of their actions as it is simply trying to capture other pieces at high risk.

#### Alpha-Beta Pruning

There is not much else to mention here, so I will end with noting that it runs much faster, which allows us to try deeper depths.

#### Iterative deepening

### Responses

####

