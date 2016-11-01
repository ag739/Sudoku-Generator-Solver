import numpy as np

"""
Generate a Sudoku board!
Using local search, the algorithm first generates a start state, and then
continues until a perfect board is achieved, or until it times out (meaning,
we've succeeded our MAXITERATIONS).
More often than not, an invalid Sudoku board is printed out.
For now, this is okay as a starting point.
TODO: look into refining the generate function.

Returns:
  SIZE**2 x SIZE**2 numpy array
"""
def generate():
  # select random initial state (initial guess at solution)
  board = np.zeros(SIZE**4).reshape(SIZE**2, SIZE**2)

  for i in range(SIZE**2):
    arr = []
    for j in range(SIZE**2):
      arr.append(j + 1)
    np.random.shuffle(arr)
    board[i] = arr

  # make local modification to improve current state
  # and continue until you reach perfect solution or run out of time
  iterations = 0
  while not perfectBoard(board) and iterations < MAXITERATIONS:
    # first check the missing and dups in square
    for i in range(SIZE**2):
      for j in range(SIZE**2):
        number = board[i, j]
        square, row, col = getSquareRowCol(board, i, j)
        # is square perfect?
        if isPerfect(square):
          # check for imperfect column
          if not isPerfect(col):
            # is this the number that repeats in the column?
            if isDuplicate(col, number):
              # get missing numbers for the column
              missing = getMissing(col)
              # get first number in the missing list that's in the same row in this box, if exists
              missing = inRowNotInCol(square, missing)
              # switch missing number and current box
              if missing != None:
                board[i] = switch(row, j, missing)
        # square is not perfect
        else:
          # is this the number that repeats in the square?
          if isDuplicate(square, number):
            # get number(s) square is missing, and pick one at random
            missing = getMissing(square)[0]
            # switch missing number and current box
            board[i] = switch(row, j, missing)

    iterations += 1
  print "Went through " + str(iterations) + " iterations"
  if not perfectBoard(board):
    print "Not a valid sudoku puzzle"
  return board

"""
Check if the board generated is a perfect Sudoku board!
A perfect Sudoku board is one that:
  for each of the squares (maximum number of non-overlapping SIZE x SIZE grids on board)
  AND
  for each row of SIZE**2 numbers
  AND
  for each column of SIZE**2 numbers,
  each number from 1 to SIZE**2, inclusive, only occurs once

Arguments:
  board: SIZE**2 x SIZE**2 numpy array
Returns:
  boolean: True if perfect board, False otherwise
"""
def perfectBoard(board):
  for i in range(SIZE):
    i = i * SIZE
    for j in range(SIZE):
      j = j * SIZE
      square, row, col = getSquareRowCol(board, i, j)
      for x in range(SIZE**2):
        if not (x+1 in square and x+1 in row and x+1 in col):
          return False
  return True

"""
Check if a SIZE by SIZE square or column is perfect (no numbers repeat)
We can easily do this by creating a unique array, and checking if the length is equal to SIZE**2

Arguments:
  arr: a numpy array, could either be SIZE x SIZE of SIZE**2 x 1
Returns:
  boolean: True if no numbers repeat
"""
def isPerfect(arr):
  arr = arr.reshape(SIZE**2,)
  return len(np.unique(arr)) == SIZE**2

"""
Check if a number is a duplicate in a numpy array

Arguments:
  lst: a numpy array
  number: integer to check in numpy array
Returns:
  boolean: True if duplicate of number exists in array, False otherwise
"""
def isDuplicate(lst, number):
  return (lst == number).sum() > 1

"""
Get the missing numbers in a numpy array
lst, in theory, should be a list of consective numbers 1 through N**2 inclusive
if lst == [4,4,1,2]:
  getMissing(lst) == [3]
if lst == [1,1,3,1]:
  getMissing(lst) == [2, 4]

Arguments:
  lst: a numpy array of size SIZE**2
Returns:
  items: the a list of missing items in the list
"""
def getMissing(lst):
  items = []
  for i in range(1,10):
    if i not in lst:
      items.append(i)
  return items

"""
For a row, switch the item that's at the current index with whichever index the missing number is

row = [4, 6, 3, 1, 2]
currIndex = 2
missingNumber = 4
new row = [3, 6, 4, 1, 2]

Arguments:
  row: numpy array with SIZE**2 indices
  currIndex: integer- index currently at
  missingNumber: integer- the number that will be switched and put at currIndex
Returns:
  row: modified row with same dimensions as original row
"""
def switch(row, currIndex, missingNumber):
  missingIndex = np.where(row == missingNumber)
  missingIndex = missingIndex[0][0]
  # if missingIndex / SIZE * SIZE == currIndex / SIZE * SIZE:
  #   return row
  row[missingIndex] = row[currIndex]
  row[currIndex] = missingNumber
  return row

"""
For a particular box on the board, board[row, col], get the square,
row, and column this box is in.

Arguments:
  board: SIZE**2 by SIZE**2 numpy array
  row: index of row
  col: index of column
Returns:
  square, row, column
  square: SIZE x SIZE numpy array
  row: a SIZE**2 array
  column: a SIZE**2 array
"""
def getSquareRowCol(board, row, col):
  i = row / SIZE * SIZE
  j = col / SIZE * SIZE
  return board[i:i+SIZE, j:j+SIZE], board[row], board[:, col]

"""
Get the first number in a list that's missing in another list
l1 = [1,3,2,1]
l2 = [1,4]
getMissingInCol(l1, l2) == 4
Arguments:
  col: numpy array with SIZE**2 entries
  missing: list with up to SIZE**2 entries
Returns:
  None if no items in missing are in col,
  else, the first item that's missing
"""
def inRowNotInCol(square, missing):
  for item in missing:
    if item in square:
      return item

"""
User can input board size: 16 boxes, or 81 boxes
"""
if __name__ == "__main__":
  # SIZE = 2
  MAXITERATIONS = 100
  # userInput = raw_input("Choose a size: 2 or 3\n")
  # SIZE = int(userInput)
  SIZE = 3
  board = generate()
  print board
