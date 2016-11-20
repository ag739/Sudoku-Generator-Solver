import sys
import solved_board as solution
import numpy as np

class Board(object):
  def __init__(self, size, maxiterations):
    self.size = size
    self.maxiterations = maxiterations
    self.solved = solution.Board(size, maxiterations).board
    self.puzzle = self.generate()

  def generate(self):
    """
    Generate a unique sudoku board that is ready to be solved!
    Systematically remove boxes while maintaining a unique solution
    """
    puzzle = self.solved.copy()
    # generate list of indices
    indices = []
    for i in range(self.size ** 2):
      for j in range(self.size ** 2):
        indices.append((i, j))
    # randomly select an index to remove
    while len(indices) > 30:
      index = indices.pop(np.random.randint(len(indices)))
      number_at_index = puzzle[index]
      puzzle[index] = 0
      # run solver on this puzzle, see if it's unique. if not, add this number back in
      # if not self.solve(puzzle):
      #   puzzle[index] = number_at_index
    return puzzle

    def getSquareRowCol(self, board, ind):
      row = ind[0]
      col = ind[1]
      i = row / self.size * self.size
      j = col / self.size * self.size
      return board[i:i+self.size, j:j+self.size], board[row], board[:, col]

    def getIndices(self, grid):
      """
      return: a list of indices in the grid where the box is empty (0), in numerical order, from smallest to largest.
        e.g. [(0, 2), (0, 8), (1, 1), (1, 3), (1,5), (2, 0), ...]
      """
      lst = []
      for i in range(self.size ** 2):
          for j in range(self.size ** 2):
              if grid[i, j] == 0:
                  lst.append((i, j))
      return lst

    def solve(self, puzzle):
      """
      grid: 9x9 numpy array
      """
      grid = puzzle.copy()
      indices = self.getIndices(grid)
      i = 0
      n = 1
      while i < len(indices):
        # get index
        ind = indices[i]
        # if empty value, try filling it in!
        if grid[ind] == 0:
          square, row, col = self.getSquareRowCol(grid, ind)
          # check if some number n is eligible
          while n < self.size ** 2 and grid[ind] == 0:
            if not (n in square or n in row or n in col):
              grid[ind] = n
            n += 1
          # if no values of n work
          if grid[ind] == 0:
            # go back to the previous index and try something new, if possible
            i -= 1
            # but if we can't increment the value anymore, go back yet another time
            while i >= 0 and grid[indices[i]] == self.size ** 2:
              # reset this value, because we're going back again
              grid[indices[i]] = 0
              i -= 1
            # and if i is out of range, we return false
            if i == -1:
              return False
            # else, reset n
            else:
              n = grid[indices[i]] + 1
              grid[indices[i]] = 0
          else:
            i += 1
            n = 1
        else:
          n = 1
          i += 1
      return True

if __name__ == "__main__":
  """
  User can input board self.size: 16 boxes, or 81 boxes
  """
  try:
    assert sys.argv[1] > 1
    size = int(sys.argv[1])
  except Exception as e:
    size = 3

  board = Board(size, 100)
  puzzle = board.puzzle
  
  s = ""
  for i in range(size ** 2):
    if i % size == 0 and not (i == 0 or i == size ** 2 - 1):
      s += "-------+-------+-------\n"
    for j in range(size ** 2):
      num = str(puzzle[i, j])[0]
      if num == "0":
        num = " "
      if j % size == 0 and not (j == 0 or j == size ** 2 -1):
        s += " | " + num
      elif j == size ** 2 - 1:
        s += " " + num + " \n"
      else:
        s += " " + num
  print s
