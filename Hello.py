import math, random
import tkinter as tk
from tkinter import ttk


window = tk.Tk()
window.title("demo")
window.geometry("300x150")

title_label = ttk.Label(master=window, text="Miles to kilometers")

window.mainloop()

width=40
height=25
totalmines=30
board=[[0 for x in range(width)] for i in range(height)]
radarsize=1

def printboard():
    COLORS = {
        1:  '\033[34m',  # Blue
        2:  '\033[32m',  # Green
        3:  '\033[31m',  # Red
        4:  '\033[94m',  # Dark Blue
        5:  '\033[35m',  # Purple
        6:  '\033[36m',  # Turquoise
        7:  '\033[30m',  # Black
        8:  '\033[37m',  # Gray
        "M":'\033[31m'   # Red
    }
    RESET = '\033[0m'
    
    for row in board:
        formatted_row = []
        for item in row:
            color = COLORS.get(item, '')  # Default to no color if item is not in COLORS
            formatted_row.append(f"{color}{item}{RESET}")
        print(' '.join(formatted_row))

for i in random.sample(range(width*height),totalmines):
    board[i//width][i%width]= "M"

for row in range(height):
	for column in range(width):
		if board[row][column]!="M":
            
			neighbours = [i[column-radarsize if column-radarsize>0 else 0:column+radarsize+1] for i in board[row-radarsize if row-radarsize>0 else 0:row+radarsize+1]]
			board[row][column] = sum(x.count("M") for x in neighbours)
printboard()
print("hello world")
print("doing")