# https://en.wikipedia.org/wiki/Mathematics_of_Sudoku
# http://www.dos486.com/sudoku/index.shtml
# https://en.wikipedia.org/wiki/Sudoku_solving_algorithms#Constraint_programming
# http://puzzling.stackexchange.com/questions/142/removing-numbers-from-a-full-sudoku-puzzle-to-create-one-with-a-unique-solution
# http://norvig.com/sudoku.html
# http://norvig.com/sudopy.shtml

import sys
import numpy as np
# This only works for 9x9 sudoku boards

def getSquareRowCol(board, row, col):
  i = row / 3 * 3
  j = col / 3 * 3
  return board[i:i+3, j:j+3], board[row], board[:, col]

def getStack(grid):
  stack = []
  for i in range(9):
      for j in range(9):
          if grid[i, j] == 0:
              stack.append((i, j))
  return stack

def backtrack(grid):
  """
  grid: 9x9 numpy array
  stack: a list of indices in the grid where the box is empty (0), in numerical order, from smallest to largest.
    e.g. [(0, 2), (0, 8), (1, 1), (1, 3), (1,5), (2, 0), ...]
  """
  stack = getStack(grid)
  i = 0
  n = 1
  while i < len(stack):
    # get index
    ind = stack[i]
    # if empty value, try filling it in!
    if grid[ind] == 0:
      square, row, col = getSquareRowCol(grid, ind[0], ind[1])
      # check if some number n is eligible
      grid[ind] = 0
      while n < 10 and grid[ind] == 0:
        if not (n in square or n in row or n in col):
          grid[ind] = n
        n += 1
      # if no values of n work
      if grid[ind] == 0:
        # go back to the previous index and try something new, if possible
        i -= 1
        # but if we can't increment the value anymore, go back yet another time
        while i >= 0 and grid[stack[i]] == 9:
          # reset this value, because we're going back again
          grid[stack[i]] = 0
          i -= 1
        # and if i is out of range, we return false
        if i == -1:
          return False
        # else, reset n
        else:
          n = grid[stack[i]] + 1
          grid[stack[i]] = 0
      else:
        i += 1
        n = 1
    else:
      n = 1
      i += 1
  return grid

def generateInitialPossibilities(puzzle):
  """
  Generate list of numbers that can potentially go in a square.
  """
  grid = np.empty([9,9], dtype='|S9')
  for i in range(9):
    for j in range(9):
      if puzzle[i, j] == 0:
        square, row, col = getSquareRowCol(puzzle, i, j)
        grid[i, j] = ''
        for k in range(1, 10):
          if not ((k in square) or (k in row) or (k in col)):
            grid[i, j] += str(k)
        # and when it's done running through...
        if len(grid[i, j]) == 1:
          grid = assignValue(grid, (i, j), grid[i, j])
          if grid is False:
            return False
      else:
        grid[i, j] = str(puzzle[i, j])[0]
  return grid

def removeValue(grid, ind, val):
  """
  grid: the puzzle
  ind: index at which you are removing a value
  val: the value that's being removed
  """
  # first make sure the value wasn't already removed
  if val not in grid[ind]:
    return grid
  # remove the value at the rows and columns
  row = ind[0]
  col = ind[1]
  # raise an error if grid at an index has no values
  # and if grid at an index has length of one, call assign value!
  # square
  for i in range(row / 3 * 3, row / 3 * 3 + 3):
    for j in range(col / 3 * 3, col / 3 * 3 + 3):
      grid[i, j] = grid[i, j].replace(val, '')
      if len(grid[i,j]) == 0:
        return False
      if len(grid[i, j]) == 1:
        grid = assignValue(grid, (i, j), grid[i, j])
  # col
  for i in range(9):
    grid[i, col] = grid[i, col].replace(val, '')
    if len(grid[i, col]) == 0:
      return False
    if len(grid[i, col]) == 1:
      grid = assignValue(grid, (i, col), grid[i, col])
  # row
  for j in range(9):
    grid[row, j] = grid[row, j].replace(val, '')
    if len(grid[row, j]) == 0:
      return False
    if len(grid[row, j] == 1):
      grid = assignValue(grid, (row, j), grid[row, j])

def assignValue(grid, ind, val):
  """
  grid: the puzzle
  ind: the index at which you are assigning a value. the index is a pair of integers, where ind[0] is the row and in[1] is the column
  val: the newly assigned value at grid[ind]
  """
  row = ind[0]
  col = ind[1]
  # remove this number that may be in this square, column, and row
  # square
  for i in range(row / 3 * 3, row / 3 * 3 + 3):
    for j in range(col / 3 * 3, col / 3 * 3 + 3):
      grid[i, j] = grid[i, j].replace(val, '')
  # col
  for i in range(9):
    grid[i, col] = grid[i, col].replace(val, '')
  # row
  for j in range(9):
    grid[row, j] = grid[row, j].replace(val, '')
  
  grid[row, col] = val
  return grid

def completedBoard(grid):
  for element in grid:
    if len(element) != 1:
      return False
  return True

def getSquareWithFewestPossibilities(grid):
  longest = 10
  val = ''
  ind = (None, None)

  for i in range(grid.shape[0]):
    for j in range(grid.shape[1]):
      element = grid[i, j]
      if len(element) <= longest:
        val = element
        ind = (i, j)
        longest = len(element)
  return val, ind

def solve(grid):
  if grid is False:
    return False
  if completedBoard(grid):
    return grid
  val, ind = getSquareWithFewestPossibilities(grid)
  # for num in val:
    # do something

if __name__ == "__main__":
  # convert string to np array
  grid_str = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
  grid = []
  for i in grid_str:
      grid.append(int(i))
  grid = np.array(grid).reshape(9,9)
  print grid
  print "\n"
  print backtrack(grid)
