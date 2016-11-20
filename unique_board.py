import sys
import solved_board as solution
import solver
import numpy as np

class Board(object):
  def __init__(self, size, maxiterations):
    self.size = size
    self.maxiterations = maxiterations
    self.solved = solution.Board(size, maxiterations).board
    self.puzzle = self.generate()

  """
  Generate a unique sudoku board that is ready to be solved!
  Systematically remove boxes while maintaining a unique solution
  """
  def generate(self):
    puzzle = self.solved.copy()
    # generate list of indices
    indices = []
    for i in range(9):
      for j in range(9):
        indices.append((i, j))
    # randomly select an index to remove
    while len(indices) > 30:
      index = indices.pop(np.random.randint(len(indices)))
      number_at_index = puzzle[index]
      puzzle[index] = 0
      # run solver on this puzzle, see if it's unique. if not, add this number back in
      # if not solver.solve(puzzle):
      #   puzzle[index] = number_at_index
    return puzzle

def getAllX(grid, x):
  """
  Returns list of indices of occurrences of 'x' in grid
  """
  lst = []
  for i in range(9):
    for j in range(9):
      if grid[i, j] == x:
        lst.append((i, j))
  return lst

"""
User can input board self.size: 16 boxes, or 81 boxes
"""
if __name__ == "__main__":
  try:
    assert sys.argv[1] > 1
    size = int(sys.argv[1])
  except Exception as e:
    size = 3

  maxiterations = 100
  board = Board(size, maxiterations)
  print board.puzzle
