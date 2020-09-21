# PA1 Report

## Jack Keane

### Initial Discussion and Introduction

The upper bound for the number of states is `(# of chickens + 1) * (# of foxes + 1) * # of possible boat locations`, which for the basic case is `4 * 4 * 2 = 32`. For the first two factors, it is dependent on the number of chickens and foxes respectively. If there are `n` chickens, then a given state could have `0, 1,...,n` chickens, which is `n+1` possibilities. The same applies for foxes. As the boat can be either on the near or far bank, there are 2 possibilities.

#### Graph of initial first two rounds of states

![graph](./pa1_states.pdf)