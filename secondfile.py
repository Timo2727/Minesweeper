import tkinter as tk
import math, random, copy

# Configuration variables
rows = 10
cols = 10
radarsize = 1
totalmines = 10

# Scale variables
button_width = 30
button_height = 30

# Game state variables
button_list = []
button_coor_list = [[0 for _ in range(cols)] for _ in range(rows)]
field_list = []
label_list = []
board = [[0 for _ in range(cols)] for _ in range(rows)]
playboard = []
mineremain = totalmines
started = False
buttonsopen = 0

# Window setup
window = tk.Tk()
window.title("Minesweeper")

# Function to print the board (for troubleshooting)
def printboard(target=board):
    COLORS = {
        1: '\033[34m',  # Blue
        2: '\033[32m',  # Green
        3: '\033[31m',  # Red
        4: '\033[94m',  # Dark Blue
        5: '\033[35m',  # Purple
        6: '\033[36m',  # Turquoise
        7: '\033[30m',  # Black
        8: '\033[37m',  # Gray
        "M": '\033[31m'  # Red
    }
    RESET = '\033[0m'

    for row in target:
        formatted_row = []
        for item in row:
            color = COLORS.get(item, '\033[37m')  # Default to gray if not a mine
            formatted_row.append(f"{color}{item}{RESET}")
        print(' '.join(formatted_row))
    print()

# Quit the game with keyboard shortcut
def quit_game(e):
    window.destroy()
window.bind('<Control-c>', quit_game)

# Handle losing the game
def lose():
    print("You lose!")
    for button in button_list:
        button.config(state=tk.DISABLED)
    tk.Label(window, text="YOU LOSE", font="Calibri 16 bold", bg="red").pack(anchor="center")

# Handle winning the game
def win():
    print("You win!")
    for button in button_list:
        button.config(state=tk.DISABLED)
    tk.Label(window, text="YOU WIN!", font="Calibri 16 bold", bg="green").pack(anchor="center")

# Ensure first click is not a mine
def first_click_guard(index):
    for y in range(rows):
        for x in range(cols):
            if board[y][x] != "M":
                board[y][x] = "M"
                break
    board[index // cols][index % cols] = 0
    calc_neighbours()
    update_field_values()

# Recursive function to open all neighboring zeros
def zero_fill(sourcey, sourcex):
    global playboard
    playboard = copy.deepcopy(board)
    stack = [(sourcey, sourcex)]

    while stack:
        sy, sx = stack.pop()
        playboard[sy][sx] = "f"

        for y in range(max(sy - radarsize, 0), min(sy + radarsize + 1, rows)):
            for x in range(max(sx - radarsize, 0), min(sx + radarsize + 1, cols)):
                if playboard[y][x] == 0:
                    stack.append((y, x))
                elif playboard[y][x] != "M":
                    playboard[y][x] = "f"

    for y in range(rows):
        for x in range(cols):
            if playboard[y][x] == "f" and button_list[y * cols + x].winfo_manager():
                open_cover(y * cols + x, fill=False)

# Handle opening a cell
def open_cover(index, fill=True):
    global buttonsopen, started

    button_list[index].place_forget()
    buttonsopen += 1
    if board[index // cols][index % cols] != "M":
        started = True
        if board[index // cols][index % cols] == 0 and fill:
            zero_fill(index // cols, index % cols)
    elif started:
        lose()
    else:
        started = True
        first_click_guard(index)
        if board[index // cols][index % cols] == 0 and fill:
            zero_fill(index // cols, index % cols)

    if cols * rows - buttonsopen == totalmines:
        win()

# Handle left-click on a button
def button_left_clicked(index):
    global mineremain
    if button_list[index].cget("text") != "⚑":
        open_cover(index)
    else:
        button_list[index].configure(text="")
        mineremain += 1

# Handle right-click to flag a cell
def right_click(event):
    global mineremain
    if event.widget.cget("text") != "⚑":
        event.widget.configure(fg="red", text="⚑", font=("Calibri", '15'))
        mineremain -= 1
    else:
        event.widget.configure(text="")
        mineremain += 1

# Calculate the number of neighboring mines
def calc_neighbours():
    for y in range(rows):
        for x in range(cols):
            if board[y][x] != "M":
                neighbours = [
                    i[max(x - radarsize, 0):min(x + radarsize + 1, cols)]
                    for i in board[max(y - radarsize, 0):min(y + radarsize + 1, rows)]
                ]
                board[y][x] = sum(row.count("M") for row in neighbours)

# Update the field values in the GUI
def update_field_values():
    for y in range(rows):
        for x in range(cols):
            index = y * cols + x
            label_list[index].configure(text=board[y][x])

# Distribute mines randomly on the board
def distribute_mines():
    mine_positions = random.sample(range(cols * rows), totalmines)
    for pos in mine_positions:
        board[pos // cols][pos % cols] = "M"

# Render the board with values
def populate_values():
    for y in range(rows):
        for x in range(cols):
            index = y * cols + x
            x_pos = x * button_width
            y_pos = y * button_height

            field = tk.Frame(window, highlightthickness=1, highlightbackground="#d4d4d4")
            field.place(x=x_pos, y=y_pos, width=button_width, height=button_height)
            label = tk.Label(field, text=board[y][x], font="Calibri 16 bold")
            label.pack()
            field_list.append(field)
            label_list.append(label)

# Render the buttons covering the cells
def populate_covers():
    for y in range(rows):
        for x in range(cols):
            index = y * cols + x
            x_pos = x * button_width
            y_pos = y * button_height
            button = tk.Button(window, borderwidth=4, command=lambda idx=index: button_left_clicked(idx))
            button.place(x=x_pos, y=y_pos, width=button_width, height=button_height)
            button.bind("<Button-2>", right_click)
            button.bind("<Button-3>", right_click)
            button_list.append(button)
            button_coor_list[y][x] = button

# Start the game
def startgame():
    window.geometry(f"{cols * button_width}x{rows * button_height}")
    distribute_mines()
    populate_values()
    populate_covers()
    printboard()
    calc_neighbours()
    update_field_values()

startgame()
window.mainloop()
