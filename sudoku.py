# GUI only works for 9x9 boards

# account for Python 2 and Python 3
try:
  import Tkinter
except Exception as e:
  import tkinter as Tkinter

from unique_board import Board


MARGIN = 20
SIDE = 50
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9

class SudokuUI(Tkinter.Frame):
  def __init__(self, parent, game):
    self.puzzle = game.puzzle
    self.solved = game.solved
    self.parent = parent
    Tkinter.Frame.__init__(self, parent)

    self.row, self.col = 0, 0

    self.__initUI()

  def __initUI(self):
    # set window title to Sudoku
    self.parent.title("Sudoku")
    # self.pack is a Frame attribute. Fill the entire frame horizontally and vertically
    self.pack(fill=Tkinter.BOTH, expand=1)
    # canvas attribute is used to display board
    self.canvas = Tkinter.Canvas(self, width=WIDTH, height=HEIGHT)
    # entire square of puzzle will fill the space and will be pulled to the top part of the window
    self.canvas.pack(fill=Tkinter.BOTH, side=Tkinter.TOP)
    # create a button to solve the board
    btn = Tkinter.Button(self, text="Give Up?", command=self.solve_board)
    # and have the button fill the space and sit at the bottom of the window
    btn.pack(fill=Tkinter.BOTH, side=Tkinter.BOTTOM)

    # draw grid
    for i in [1, 2, 4, 5, 7, 8, 0, 3, 6, 9]:
      color = "black" if i % 3 == 0 else "gray"

      x0 = MARGIN + i * SIDE
      y0 = MARGIN
      x1 = MARGIN + i * SIDE 
      y1 = HEIGHT - MARGIN
      self.canvas.create_line(x0, y0, x1, y1, fill=color)

      x0 = MARGIN
      y0 = MARGIN + i * SIDE
      x1 = WIDTH - MARGIN
      y1 = MARGIN + i * SIDE 
      self.canvas.create_line(x0, y0, x1, y1, fill=color)

    # draw_puzzle()
    for i in range(9):
      for j in range(9):
        num = int(self.puzzle[i, j])
        if num != 0:
          x = MARGIN + j * SIDE + SIDE / 2
          y = MARGIN + i * SIDE + SIDE / 2
          self.canvas.create_text(x, y, text = num, fill='black')
        else:
          self.canvas.create_rectangle(x0, y0, x1, y1)

    self.canvas.focus_set()
    # bind a left mouse click (<Button-2> is center, <Button-3> is right) to a function cell_clicked
    self.canvas.bind("<Button-1>", self.cell_click)
    # binds a user key press to the key_pressed function
    self.canvas.bind("<Key>", self.key_press)

  def solve_board(self):
    for i in range(9):
      for j in range(9):
        if self.puzzle[i, j] == 0:
          num = int(self.solved[i, j])
          x = MARGIN + j * SIDE + SIDE / 2
          y = MARGIN + i * SIDE + SIDE / 2
          self.canvas.create_text(x, y, text = num, fill='blue')
          self.puzzle[i, j] = self.solved[i, j]

  def cell_click(self, event):
    # remove previous cell click
    self.canvas.delete("selected")

    x, y = event.x, event.y
    if MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN:
      # get row and col
      self.row, self.col = (y - MARGIN) / SIDE, (x - MARGIN) / SIDE
      # only select a row that's not filled in
      if self.puzzle[self.row, self.col] == 0:
        x0 = MARGIN + self.col * SIDE + 1
        y0 = MARGIN + self.row * SIDE + 1
        x1 = MARGIN + (self.col + 1) * SIDE - 1
        y1 = MARGIN + (self.row + 1) * SIDE - 1
        self.canvas.create_rectangle(x0, y0, x1, y1, outline="medium blue", tags="selected")
      else:
        num = self.puzzle[self.row, self.col]
        indices = getAllX(self.puzzle, num)
        for index in indices:
          x0 = MARGIN + index[1] * SIDE + 1
          y0 = MARGIN + index[0] * SIDE + 1
          x1 = MARGIN + (index[1] + 1) * SIDE - 1
          y1 = MARGIN + (index[0] + 1) * SIDE - 1
          self.canvas.create_rectangle(x0, y0, x1, y1, fill="alice blue", outline="alice blue", tags="selected")

          x = MARGIN + index[1] * SIDE + SIDE / 2
          y = MARGIN + index[0] * SIDE + SIDE / 2
          self.canvas.create_text(x, y, text = int(num), fill='blue', tags="selected")
    else:
      self.row, self.col = -1, -1

  def key_press(self, event):
    if self.row >= 0 and self.col >= 0 and event.char in "123456789":
      if self.solved[self.row, self.col] == int(event.char) and self.puzzle[self.row, self.col] == 0:
        # draw the character
        x = MARGIN + self.col * SIDE + SIDE / 2
        y = MARGIN + self.row * SIDE + SIDE / 2
        self.canvas.create_text(x, y, text = event.char, fill='blue')
        self.puzzle[self.row, self.col] = int(event.char)
        self.canvas.delete("selected")
      else:
        if self.puzzle[self.row, self.col] != 0:
          print "Already filled in!"
        elif self.solved[self.row, self.col] != int(event.char):
          print "Wrong number!"
        self.canvas.delete("selected")

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

if __name__ == "__main__":
  board = Board(3, 100, 35)
  root = Tkinter.Tk()
  SudokuUI(root, board)
  root.geometry(str(WIDTH) + 'x' + str(HEIGHT + SIDE))
  root.mainloop()