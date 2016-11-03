import unique_board

"""
Solve a Sudoku board!
"""
def solve():
  solution = unique_board.getPerfectBoard()
  board = unique_board.generate(solution)
  return board
