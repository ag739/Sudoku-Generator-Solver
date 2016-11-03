import solved_board

"""
Generate a unique sudoku board that is ready to be solved!
Systematically remove boxes while maintaining a unique solution
"""
def generate(board):
  return board

"""
Get a perfect board
Returns:
  board: SIZE**2 x SIZE**2 numpy array that is a perfect Sudoku board
"""
def getPerfectBoard():
  while True:
    board = solved_board.generate()
    if solved_board.perfectBoard(board):
      return board 

"""
See getSquareRowCol from solved_board.py
"""
def getSquareRowCol(board, row, col):
  return solved_board.getSquareRowCol(board, row, col)
