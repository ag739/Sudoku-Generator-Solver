import numpy as np
import sys

class Board(object):
  def __init__(self, size, maxiterations):
    self.size = size
    self.maxiterations = maxiterations
    self.board = self.getPerfectBoard()

  """
  Generate generates a solved Sudoku board (unless it runs out of time)
  getPerfectBoard will keep trying generate until a perfect board is generated
  Returns:
    board: SIZE**2 x SIZE**2 numpy array that is a perfect Sudoku board
  """
  def getPerfectBoard(self):
    while True:
      b = self.generate()
      if self.perfectBoard(b):
        return b

  """
  Generate a solved Sudoku board!
  Using local search, the algorithm first generates a start state, and then
  continues until a perfect board is achieved, or until it times out (meaning,
  we've succeeded our self.maxiterations).
  More often than not, an invalid Sudoku board is printed out.
  For now, this is okay as a starting point.
  TODO: look into refining the generate function.

  Returns:
    self.size**2 x self.size**2 numpy array
  """
  def generate(self, step=False):
    # select random initial state (initial guess at solution)
    board = np.zeros(self.size**4).reshape(self.size**2, self.size**2)

    for i in range(self.size**2):
      arr = []
      for j in range(self.size**2):
        arr.append(j + 1)
      np.random.shuffle(arr)
      board[i] = arr

    # make local modification to improve current state
    # and continue until you reach perfect solution or run out of time
    iterations = 0
    while not self.perfectBoard(board) and iterations < self.maxiterations:
      if step:
        print "At iteration " + str(iterations)
        print board
        user_input = raw_input("Continue? (Y or N) >> ")
        if user_input != 'y':
          return board

      board = self.localSearch(board, iterations)
      iterations += 1

    if step:
      print "Went through " + str(iterations) + " iterations"
    if not self.perfectBoard(board):
      if step:
        print "Not a valid sudoku puzzle"
    return board

  """
  Helper function for generate board
  """
  def localSearch(self, board, iterations):
    # first check the missing and dups in square
    for i in range(self.size**2):
      for j in range(self.size**2):
        number = board[i, j]
        square, row, col = self.getSquareRowCol(board, i, j)
        # is square perfect?
        if self.isPerfect(square):
          # check for imperfect column
          if not self.isPerfect(col):
            # is this the number that repeats in the column?
            if self.isDuplicate(col, number):
              # get missing numbers for the column
              missing = self.getMissing(col)
              # get first number in the missing list that's in the same row in this box, if exists
              missing = self.inRowNotInCol(square[i % self.size], missing)
              # switch missing number and current box
              if missing != None:
                board[i] = self.switch(row, j, missing)
            # generate some probability that we switch anyways
            else:
              if np.random.rand() < (self.maxiterations - iterations + 0.) / self.maxiterations:
                missing = self.getMissing(col)[0]
                board[i] = self.switch(row, j, missing)
        # square is not perfect
        else:
          # is this the number that repeats in the square?
          if self.isDuplicate(square, number):
            # get number(s) square is missing, and pick one at random
            missing = self.getMissing(square)[0]
            # switch missing number and current box
            board[i] = self.switch(row, j, missing)
    return board

  """
  Check if the board generated is a perfect Sudoku board!
  A perfect Sudoku board is one that:
    for each of the squares (maximum number of non-overlapping self.size x self.size grids on board)
    AND
    for each row of self.size**2 numbers
    AND
    for each column of self.size**2 numbers,
    each number from 1 to self.size**2, inclusive, only occurs once

  Arguments:
    board: self.size**2 x self.size**2 numpy array
  Returns:
    boolean: True if perfect board, False otherwise
  """
  def perfectBoard(self, board):
    for i in range(self.size):
      i = i * self.size
      for j in range(self.size):
        j = j * self.size
        square, row, col = self.getSquareRowCol(board, i, j)
        for x in range(self.size**2):
          if not (x+1 in square and x+1 in row and x+1 in col):
            return False
    return True

  """
  Check if a self.size by self.size square or column is perfect (no numbers repeat)
  We can easily do this by creating a unique array, and checking if the length is equal to self.size**2

  Arguments:
    arr: a numpy array, could either be self.size x self.size of self.size**2 x 1
  Returns:
    boolean: True if no numbers repeat
  """
  def isPerfect(self, arr):
    arr = arr.reshape(self.size**2,)
    return len(np.unique(arr)) == self.size**2

  """
  Check if a number is a duplicate in a numpy array

  Arguments:
    lst: a numpy array
    number: integer to check in numpy array
  Returns:
    boolean: True if duplicate of number exists in array, False otherwise
  """
  def isDuplicate(self, lst, number):
    return (lst == number).sum() > 1

  """
  Get the missing numbers in a numpy array
  lst, in theory, should be a list of consective numbers 1 through N**2 inclusive
  if lst == [4,4,1,2]:
    getMissing(lst) == [3]
  if lst == [1,1,3,1]:
    getMissing(lst) == [2, 4]

  Arguments:
    lst: a numpy array of self.size self.size**2
  Returns:
    items: the a list of missing items in the list
  """
  def getMissing(self, lst):
    items = []
    for i in range(1,self.size**2 + 1):
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
    row: numpy array with self.size**2 indices
    currIndex: integer- index currently at
    missingNumber: integer- the number that will be switched and put at currIndex
  Returns:
    row: modified row with same dimensions as original row
  """
  def switch(self, row, currIndex, missingNumber):
    missingIndex = np.where(row == missingNumber)
    missingIndex = missingIndex[0][0]
    # if missingIndex / self.size * self.size == currIndex / self.size * self.size:
    #   return row
    row[missingIndex] = row[currIndex]
    row[currIndex] = missingNumber
    return row

  """
  For a particular box on the board, board[row, col], get the square,
  row, and column this box is in.

  Arguments:
    board: self.size**2 by self.size**2 numpy array
    row: index of row
    col: index of column
  Returns:
    square, row, column
    square: self.size x self.size numpy array
    row: a self.size**2 array
    column: a self.size**2 array
  """
  def getSquareRowCol(self, board, row, col):
    i = row / self.size * self.size
    j = col / self.size * self.size
    return board[i:i+self.size, j:j+self.size], board[row], board[:, col]

  """
  Get the first number in a list that's missing in another list
  l1 = [1,3,2,1]
  l2 = [1,4]
  getMissingInCol(l1, l2) == 4
  Arguments:
    col: numpy array with self.size**2 entries
    missing: list with up to self.size**2 entries
  Returns:
    None if no items in missing are in col,
    else, the first item that's missing
  """
  def inRowNotInCol(self, square, missing):
    for item in missing:
      if item in square:
        return item

  """
  Test how many perfect boards we get
  """
  def test():
    perfect = 0.
    for i in range(self.maxiterations):
      b = generate()
      if perfectBoard(b):
        perfect += 1
    print perfect / self.maxiterations

"""
User can input board self.size: 16 boxes, or 81 boxes
"""
if __name__ == "__main__":
  try:
    assert sys.argv[1] > 1
    size = int(sys.argv[1])
  except Exception as e:
    size = 2

  maxiterations = 100
  board = Board(size, maxiterations).board
  print board

  # # test how many perfect boards we get...
  # test()
