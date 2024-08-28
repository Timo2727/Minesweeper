import tkinter as tk
import math, random, copy

#config variables
rows = 16
cols = 16
radarsize=1
totalmines=28

#scale variables
button_width = 30
button_height = 30

#empty list definitions
button_list = []
button_coor_list= [[0 for x in range(cols)] for i in range(rows)]
field_list=[]
lable_list=[]
board=[[0 for x in range(cols)] for i in range(rows)]
playboard=[]


#tag variable definitions
mineremain=totalmines
started=False
buttonsopen=0

#Window setup
window = tk.Tk()
window.title("MINESWEEPER")


#menu screen to configure game settings
def menu():
    window.geometry("400x400")

    tk.Label(window,text="Board Dimensions").pack()
    tk.Label(window,text="x").pack(side="right")
    dim_inp=tk.Entry(window)
    dim_inp.pack()

    var=tk.IntVar()
    start=tk.Button(window, text="Play!", command=lambda: var.set(1))
    start.pack() 

    start.wait_variable(var)
    startgame()



#print board troubleshooting function
def printboard(target=board):
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
    
    for row in target:
        formatted_row = []
        for item in row:
            color = COLORS.get(item, '') if item == "M" else '\033[37m'
            formatted_row.append(f"{color}{item}{RESET}")
        print(' '.join(formatted_row))
    print()

#quit keyboard shortcut
def quit(e):
     window.destroy()
window.bind('<Control-c>', quit)

#Landed on a mine
def lose():
    print("you lose")
    for i in button_list:
        i.config(state=tk.DISABLED) 
    tk.Label(window,text= "YOU LOSE", font="Calibri 16 bold", bg= "red").pack(anchor="center")

#Won the game
def win():
    print("you win!")
    for i in button_list:
        i.config(state=tk.DISABLED) 
    tk.Label(window,text= "YOU WIN!", font="Calibri 16 bold", bg= "green").pack(anchor="center")
     

#if first click is a mine
def first_click_guard(index):
    stop=False
    for y in range(rows):
        for x in range(cols):
            if board[y][x]!="M":
                board[y][x]="M"
                stop=True
                break
        if stop: break
    board[index//cols][index%cols]=0   
    calc_neighbours()
    update_field_values()





#recursive function that opens all buttons covering neighboring 0s if source is 0
def zero_fill(sourcey, sourcex):
    global recursions
    recursions = 0  # Reset recursions counter
    stack = [(sourcey, sourcex)]  # Initialize stack with the starting cell

    while stack:
        sy, sx = stack.pop()
        if recursions > 500:
            continue

        playboard[sy][sx] = "f"
        recursions += 1

        # Define the range for the neighbors
        start_y = max(sy - radarsize, 0)
        end_y = min(sy + radarsize + 1, len(playboard))
        start_x = max(sx - radarsize, 0)
        end_x = min(sx + radarsize + 1, len(playboard[0]))

        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                if playboard[y][x] == 0:
                    # Push the neighbor onto the stack if it's 0
                    stack.append((y, x))












#if cover clicked               
def button_left_clicked(index):
   global started
   global mineremain
   global buttonsopen
   global playboard
   global recursions
   if button_list[index].cget("text")!="⚑":
 

        button_list[index].place_forget()
        buttonsopen+=1
        if board[index//cols][index%cols]!="M":
            started=True
            if board[index//cols][index%cols]==0:
                playboard = board.copy()
                recursions=0
                zero_fill(index//cols, index%cols)
                printboard(target=playboard)
        elif started:
            lose()
            lost=True
        else:
            started=True
            first_click_guard(index)
        printboard(target=board)
        if cols*rows-buttonsopen==totalmines and not "lost" in locals():
            win() 


    else:
        button_list[index].configure(text="")
        mineremain+=1
    print(mineremain)
    

#(FLAG) if cover right-clicked
def right_click(event):
    global mineremain
    if event.widget.cget("text")!="⚑":
        event.widget.configure(fg="red", text="⚑", font=("Calibri", '15'))
        mineremain-=1
    else:
        event.widget.configure(text="")
        mineremain+=1
    print(mineremain)

#calculate neighbour values in board list
def calc_neighbours():
    for row in range(rows):
        for column in range(cols):
            if board[row][column]!="M":
                
                neighbours = [i[column-radarsize if column-radarsize>0 else 0:column+radarsize+1] for i in board[row-radarsize if row-radarsize>0 else 0:row+radarsize+1]]
                board[row][column] = sum(x.count("M") for x in neighbours)

#update tkinter frames to match board values  
def update_field_values():            
    for y in range(rows):
        for x in range(cols):
            index = y * cols + x
            lable_list[index].configure(text=board[y][x])


#distribute Mines
def distribute_mines():
    for i in random.sample(range(cols*rows),totalmines):
        board[i//cols][i%cols]= "M"


#Tkinter render board field values as tkinter frames
def populate_values():
    for y in range(rows):
        for x in range(cols):
            index = y * cols + x
            x_pos = x * button_width
            y_pos = y * button_height
            
            field = tk.Frame(window, highlightthickness=1, highlightbackground="#d4d4d4")
            field.place(x=x_pos, y=y_pos, width=button_width, height=button_height)
            lable = tk.Label(field, text=board[y][x], font="Calibri 16 bold")
            lable.pack()
            field_list.append(field)
            lable_list.append(lable)

#Tkinter render cover Buttons
def populate_covers(target="all"):
    for y in range(rows):
        for x in range(cols):
            index = y * cols + x
            x_pos = x * button_width
            y_pos = y * button_height
            button = tk.Button(window, borderwidth=4 ,command=lambda idx=index: button_left_clicked(idx))
            button.place(x=x_pos, y=y_pos, width=button_width, height=button_height)
            button.bind("<Button-2>", right_click)
            button.bind("<Button-3>", right_click)
            button_list.append(button)
            button_coor_list[y][x]=button

def startgame():
    window.geometry(str(str(cols*button_width)+"x"+str(rows*button_height)))
    distribute_mines()
    populate_values()
    populate_covers() 
    printboard()
    calc_neighbours()
    update_field_values()

startgame()



window.mainloop()