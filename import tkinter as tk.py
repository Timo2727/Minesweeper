import tkinter as tk

window = tk.Tk()
window.title("hello")

window.geometry("500x500")

blue_frame = tk.Frame(window, bg="blue", width=100, height=200)
red_frame = tk.Frame(window, bg="red", width=10, height=20)
# Pack the frame with the desired alignment
blue_frame.pack(side="right", padx=3)
red_frame.pack(side="left")


window.mainloop()