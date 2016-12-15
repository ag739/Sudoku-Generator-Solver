# Sudoku Puzzle Generator and Solver
_For CS 4701 - Practicum in Artificial Intelligence_

Project looking at algorithms to generate full Sudoku boards and a Sudoku puzzle solver. The full Sudoku board generation must first generate a full, complete board, and then must determine which boxes to remove while still maintaining a unique puzzle.

## Generate a full, complete board
Running `python solved_board.py` will print out the numpy array of the board as well as a formatted version of the completed board.

```
[[ 6.  2.  3.  1.  7.  5.  9.  8.  4.]
 [ 7.  4.  5.  9.  8.  2.  1.  6.  3.]
 [ 1.  8.  9.  6.  4.  3.  2.  7.  5.]
 [ 2.  9.  8.  3.  6.  7.  4.  5.  1.]
 [ 4.  1.  7.  8.  5.  9.  6.  3.  2.]
 [ 5.  3.  6.  2.  1.  4.  8.  9.  7.]
 [ 9.  6.  4.  7.  3.  1.  5.  2.  8.]
 [ 3.  5.  2.  4.  9.  8.  7.  1.  6.]
 [ 8.  7.  1.  5.  2.  6.  3.  4.  9.]]
 6 2 3 | 1 7 5 | 9 8 4
 7 4 5 | 9 8 2 | 1 6 3
 1 8 9 | 6 4 3 | 2 7 5
-------+-------+-------
 2 9 8 | 3 6 7 | 4 5 1
 4 1 7 | 8 5 9 | 6 3 2
 5 3 6 | 2 1 4 | 8 9 7
-------+-------+-------
 9 6 4 | 7 3 1 | 5 2 8
 3 5 2 | 4 9 8 | 7 1 6
 8 7 1 | 5 2 6 | 3 4 9
```

### Optional arguments
_n_: number of units in each _n_ x _n_ square
Default is three, so `python solved_board.py` is the same thing as `python solved_board.py 3`

## Generate a unique puzzle
Running `python unique_board.py` will print out a formatted version of the puzzle. The print statements in the console denote how many more indices the generator will try to remove while still maintaining a unique puzzle.

```
 7     |   2 9 |
     8 | 3 6 7 | 1 4
 9   1 | 5 8   | 7
-------+-------+-------
       |       |   3
 1     |   4 3 | 8   2
   6   | 2   5 |
-------+-------+-------
 3 8 4 |   5 6 |
 6   2 | 7 3   |     5
 5 7   |       | 3   8
```

### Optional arguments
_n_: number of units in each _n_ x _n_ square
Default is three, so `python unique_board.py` is the same thing as `python unique_board.py 3`
_threshold_: number of indices the generator will try to remove from the complete board
Default is 35, so `python unique_board.py` is the same thing as `python unique_board.py 3 35`

## Solve a Sudoku Puzzle using the GUI
Run `python sudoku.py` to use the GUI.
An incorrect guess is not allowed by the GUI, and the console will warn you when you make an incorrect guess.

### Optional arguments
There are no option arguments. The GUI only supports a 9x9 board at the moment.
