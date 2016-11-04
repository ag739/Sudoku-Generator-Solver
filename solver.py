import sys
import unique_board as ub

class Solver(object):
  def __init__(self, size, maxiterations):
    self.size = size
    self.maxiterations = maxiterations
    board = ub.Board(size, maxiterations)
    self.solved = board.solved
    self.puzzle = board.puzzle

  """
  Solve a Sudoku board!
  """
  def solve(self):
    return self.solved

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
  board = Solver(size, maxiterations).solved
  print board