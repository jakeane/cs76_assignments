# PA3: Chess README

## COSC 76 20F

## Jack Keane

### Set up environment

```
virtualenv env
source env/bin/activate
pip3 install python-chess
pip3 install pyqt5
pip3 install numpy
```
My environment also had autopep8, pycodestyle, and toml for some reason, but I do not think the program is dependent on them.

### To run

Simply running `test_chess.py` or `gui_chess.py` will work as long as there are two agents in lines 16-17 for `test_chess.py` and lines 75-76 for `gui_chess.py`.

### Agents

- `MinimaxAI(depth: int, is_white: bool, (optional) use_book: bool)`
- `AlphaBetaAI(depth: int, is_white: bool, (optional) use_book: bool)`
    - Note: line 46 can be commented out, but I am not sure if that loses optimality
- `SortAlphaBetaAI(depth: int, is_white: bool, (optional) use_book: bool)`
- `NonOptAlphaBetaAI(depth: int, is_white: bool, (optional) use_book: bool)`
- `IterativeAlphaBetaAI(is_white: bool, time_limit: int, (optional) use_book: bool)`
- `NullAlphaBetaAI(is_white: bool, time_limit: int, (optional) use_book: bool)`
- `TranspoIterativeAlphaBetaAI(is_white: bool, time_limit: int, (optional) use_book: bool)`
