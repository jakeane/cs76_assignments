# PA6: Hidden Markov Models README

## Jack Keane

### To run

There are 3 command-line parameters to the program `HMMMaze.py`:

- The `.maz` file that represents the maze.
  - Walls are represented with '#'
  - The maze is assumed to be rectangular
- An integer where:
  - If `0`, then it will do the filtering algorithm
  - If otherwise, then it will do the Viterbi algorithm
- An integer for the length of the sequence generated
  - Must be positive
