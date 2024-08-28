import tkinter as tk
import math, random

window = tk.Tk()
window.title("MINESWEEPER")

window.geometry("400x400")

tk.Label(window,text="Board Dimensions").pack()
tk.Label(window,text="x").pack(side="right")
dim_inp=tk.Entry(window)
dim_inp.pack()

var=tk.IntVar()
start=tk.Button(window, text="Play!", command=lambda: var.set(1))
start.pack() 

#start.wait_variable(var)


button_list = []
field_list=[]
lable_list=[]


button_width = 30
button_height = 30
rows = 7
cols = 7
window.geometry(str(str(cols*button_width)+"x"+str(rows*button_height)))

radarsize=1
totalmines=28
mineremain=totalmines
board=[[0 for x in range(cols)] for i in range(rows)]
started=False
buttonsopen=0






#print board troubleshooting function
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
            color = COLORS.get(item, '') if item == "M" else '\033[37m'
            formatted_row.append(f"{color}{item}{RESET}")
        print(' '.join(formatted_row))

#quit keyboard shortcut
def quit(e):
     window.destroy()
window.bind('<Control-c>', quit)

#Landed on a mine
def loose():
    print("you loose")
    for i in button_list:
        i.config(state=tk.DISABLED) 
    tk.Label(window,text= "YOU LOOSE", font="Calibri 16 bold", bg= "red").pack(anchor="center")

#Won the game
def win():
    print("you win!")
    for i in button_list:
        i.config(state=tk.DISABLED) 
    tk.Label(window,text= "YOU WIN!", font="Calibri 16 bold", bg= "green").pack(anchor="center")
     
    

#if first click is a mine
def startclick(index):
    stop=False
    for y in range(rows):
        for x in range(cols):
            if board[y][x]!="M":
                board[y][x]="M"
                stop=True
                break
        if stop: break
    board[index//cols][index%cols]=0   
    calc()

#if cover clicked               
def hidebutton(index):
    global started
    global mineremain
    global buttonsopen
    if button_list[index].cget("bg")!="red":
 

        button_list[index].place_forget()
        buttonsopen+=1
        if board[index//cols][index%cols]!="M":
            started=True
        elif started:
            loose()
            lost=True
        else:
            started=True
            startclick(index)
        printboard()
        print()
        if cols*rows-buttonsopen==totalmines and not "lost" in locals():
            win() 


    else:
        button_list[index].configure(bg="SystemButtonFace", text="")
        mineremain+=1
    print(mineremain)
    

#(FLAG) if cover right-clicked
def right_click(event):
    global mineremain
    if event.widget.cget("bg")!="red":
        event.widget.configure(bg="red", text="F")
        mineremain-=1
    else:
        event.widget.configure(bg="SystemButtonFace", text="")
        mineremain+=1
    print(mineremain)


def calc():
    #calculate neighbour values in board list
    for row in range(rows):
        for column in range(cols):
            if board[row][column]!="M":
                
                neighbours = [i[column-radarsize if column-radarsize>0 else 0:column+radarsize+1] for i in board[row-radarsize if row-radarsize>0 else 0:row+radarsize+1]]
                board[row][column] = sum(x.count("M") for x in neighbours)

    #update tkinter frames to match board values             
    for y in range(rows):
        for x in range(cols):
            index = y * cols + x
            lable_list[index].configure(text=board[y][x])








#distribute Mines
for i in random.sample(range(cols*rows),totalmines):
    board[i//cols][i%cols]= "M"


#Tkinter render board field values as tkinter frames
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
for y in range(rows):
    for x in range(cols):
        index = y * cols + x
        x_pos = x * button_width
        y_pos = y * button_height
        button = tk.Button(window, borderwidth=4 ,command=lambda idx=index: hidebutton(idx))
        button.place(x=x_pos, y=y_pos, width=button_width, height=button_height)
        button.bind("<Button-2>", right_click)
        button.bind("<Button-3>", right_click)
        button_list.append(button)



printboard()
print()
calc()

window.mainloop()
