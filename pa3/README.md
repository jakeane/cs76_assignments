# PA3: Chess README

## COSC 76 20F

## Jack Keane

### Set up environment

```
virtualenv env
source env/bin/activate
pip3 install chess
pip3 install pyqt
pip3 install numpy
```

### To run

Simply running `test_chess.py` or `gui_chess.py` will work as long as there are two agents in lines 16-17 for `test_chess.py` and lines 75-76 for `gui_chess.py`.

### Agents

- `MinimaxAI(depth: int, is_white: bool)`
- `AlphaBetaAI(depth: int, is_white: bool)`
- `SortAlphaBetaAI(depth: int, is_white: bool)`
- `NonOptAlphaBetaAI(depth: int, is_white: bool)`
- `IterativeAlphaBetaAI(is_white: bool, time_limit: int)`
