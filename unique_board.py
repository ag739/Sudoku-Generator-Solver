import sys
import solved_board as sb

class Board(object):
  def __init__(self, size, maxiterations):
    self.size = size
    self.maxiterations = maxiterations
    self.solved = sb.Board(size, maxiterations).board
    self.puzzle = self.generate()

  """
  Generate a unique sudoku board that is ready to be solved!
  Systematically remove boxes while maintaining a unique solution
  """
  def generate(self):
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
  board = Board(size, maxiterations).solved
  print board
