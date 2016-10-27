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
        # check square
        if isDuplicate(square, number):
          # get what's missing
          missing = getMissing(square)
          # and switch
          board[i] = switch(row, j, missing)
        elif isDuplicate(col, number):
          # get what's missing
          missing = getMissing(col)
          # and switch
          board[i] = switch(row, j, missing)
        # and continue...
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
Get the first missing number in a numpy array
lst, in theory, should be a list of consective numbers 1 through N**2 inclusive
if lst == [4,4,1,2]:
  getMissing(lst) == 3

Arguments:
  lst: a numpy array of size SIZE**2
Returns:
  integer: the first missing number in lst
"""
def getMissing(lst):
  found = False
  item = 1
  while not found:
    if not item in lst:
      found = True
    else:
      item += 1
  return item

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
  # if the missing index in this row is in the same box as the current index
  # do nothing
  if missingIndex / SIZE * SIZE == currIndex / SIZE * SIZE:
    return row
  else:
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
User can input board size: 16 boxes, or 81 boxes
"""
if __name__ == "__main__":
  # SIZE = 2
  MAXITERATIONS = 100
  userInput = raw_input("Choose a size: 2 or 3\n")
  SIZE = int(userInput)
  board = generate()
  print board
