import numpy as np
# This only works for 9x9 sudoku boards

def getSquareRowCol(board, row, col):
  i = row / 3 * 3
  j = col / 3 * 3
  return board[i:i+3, j:j+3], board[row], board[:, col]

def getStack(grid):
  """
  stack: a list of indices in the grid where the box is empty (0), in numerical order, from smallest to largest.
    e.g. [(0, 2), (0, 8), (1, 1), (1, 3), (1,5), (2, 0), ...]
  """
  stack = []
  for i in range(9):
      for j in range(9):
          if grid[i, j] == 0:
              stack.append((i, j))
  return stack

def backtrack(grid):
  """
  grid: 9x9 numpy array
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
