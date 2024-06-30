import tkinter as tk
from tkinter import messagebox
import numpy as np
import random

CSize = 60
BSize = 8

Moves = [(-2, -1), (-2, 1), (2, -1), (2, 1), (1, 2), (1, -2), (-1, -2),
         (-1, 2)]


class KnightGUI:

  def __init__(self, root):
    self.root = root
    self.root.title("Knight's Project")

    self.canvas = tk.Canvas(root, width=480, height=480)
    self.canvas.pack()

    self.start_button = tk.Button(root, text="Start", command=self.Start_btn)
    self.start_button.pack(pady=8)

    self.label = tk.Label(root, text="Press start after selecting a position:")
    self.label.pack()

    self.board = np.zeros((BSize, BSize), dtype=int)
    self.Current_position = 0

    self.canvas.bind("<Button-1>", self.Clicked)

    self.draw_board()

  def Clicked(self, event):
    row = event.y // CSize
    col = event.x // CSize

    self.Current_position = [row, col]
    self.board[self.Current_position[0], self.Current_position[1]] = 1
    self.draw_board()
    self.draw_cell(self.Current_position[0], self.Current_position[1])

  def Start_btn(self):
    if self.Current_position == 0:
      messagebox.showerror("No location selected",
                           "Select a location to start.")
      return

    Option = self.Select_method()

  def Select_method(self):
    Option_tab = tk.Toplevel(self.root)
    Option_tab.title("Select Step 1 or Step 2")
    label = tk.Label(Option_tab, text="Select An Option:")
    label.pack()

    step1_button = tk.Button(Option_tab,
                             text="Step 1",
                             command=lambda: self.run_Option(1))
    step1_button.pack(pady=8)

    step2_button = tk.Button(Option_tab,
                             text="Step 2",
                             command=lambda: self.run_Option(2))
    step2_button.pack(pady=8)

  def run_Option(self, Option):

    self.root.after(2500)
    if Option == 1:
      self.knight_1step()
    elif Option == 2:
      self.knight_2step()

  def knight_1step(self):
    visited = np.zeros((BSize, BSize), dtype=bool)
    visited[self.Current_position[0], self.Current_position[1]] = True

    for move in range(2, BSize**2 + 1):
      next_moves = self.Possible_moves(self.Current_position[0],
                                       self.Current_position[1], visited)

      if (not next_moves) or (move >= 65):
        messagebox.showinfo("Tour Completed", "Knight visited all the cells!")
        return

      if len(next_moves) > 1:
        next_moves = sorted(next_moves,
                            key=lambda x: -self.count_available_moves(
                              x[0], x[1]))  # Sort in descending order

      next_pos = next_moves[0]
      self.Current_position = next_pos
      visited[next_pos[0], next_pos[1]] = True
      self.board[next_pos[0], next_pos[1]] = move
      self.draw_cell(next_pos[0], next_pos[1])
      self.root.update()
      self.root.after(500)

  def knight_2step(self):
    visited = np.zeros((BSize, BSize), dtype=bool)
    visited[self.Current_position[0], self.Current_position[1]] = True

    move = 2
    while move <= BSize**2:
      next_moves = self.Possible_moves(self.Current_position[0],
                                       self.Current_position[1], visited)

      if (not next_moves) or (move >= 65):
        messagebox.showinfo("Tour Completed", "Knight visited all the cells!")
        return

      if len(next_moves) > 1:
        next_moves = sorted(next_moves,
                            key=lambda x: -self.count_available_moves(
                              x[0], x[1]))  # Sort in descending order

      next_pos = next_moves[0]
      self.Current_position = next_pos
      visited[next_pos[0], next_pos[1]] = True
      self.board[next_pos[0], next_pos[1]] = move
      self.draw_cell(next_pos[0], next_pos[1])
      self.root.update()
      self.root.after(500)

      next_next_moves = self.Possible_moves(next_pos[0], next_pos[1], visited)
      if next_next_moves:
        next_next_pos = min(next_next_moves,
                            key=lambda x: -self.count_available_moves(
                              x[0], x[1]))  # Sort in descending order
        self.Current_position = next_next_pos
        visited[next_next_pos[0], next_next_pos[1]] = True
        self.board[next_next_pos[0], next_next_pos[1]] = move + 1
        self.draw_cell(next_next_pos[0], next_next_pos[1])
        self.root.update()
        self.root.after(500)

      move += 2

  def Possible_moves(self, row, col, visited):
    moves = []
    for move in Moves:
      next_row = row + move[0]
      next_col = col + move[1]
      if self.Valid(next_row, next_col) and not visited[next_row, next_col]:
        moves.append((next_row, next_col))
    return moves

  def Valid(self, row, col):
    return 0 <= row < BSize and 0 <= col < BSize

  def count_available_moves(self, row, col):

    available_moves = []
    for move in Moves:
      next_row = row + move[0]
      next_col = col + move[1]
      if self.Valid(next_row, next_col) and not self.board[next_row, next_col]:
        available_moves.append((next_row, next_col))
    return len(available_moves)

  def draw_board(self):

    for row in range(BSize):
      for col in range(BSize):
        x1 = col * CSize
        y1 = row * CSize
        x2 = x1 + CSize
        y2 = y1 + CSize
        color = "sea green" if (row + col) % 2 == 0 else "pale green"
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

  def draw_cell(self, row, col):
    x = col * CSize
    y = row * CSize
    x2 = x + CSize
    y2 = y + CSize
    self.canvas.create_oval(x + 8, y + 8, x2 - 8, y2 - 8, fill="black")
    self.canvas.create_text(x + CSize // 2,
                            y + CSize // 2,
                            text=str(self.board[row, col]),
                            fill="white")

    knight_image = tk.PhotoImage(file="Knight.png")
    resized_image = knight_image.subsample(4)
    self.canvas.create_image(x + CSize // 2,
                             y + CSize // 2,
                             image=resized_image)

    self.canvas.image = resized_image


root = tk.Tk()
KnightGUI(root)
root.mainloop()
# if it doesnt run. run it in replit.