from tkinter import *

COLOR1, COLOR2, COLOR3, COLOR4 = '#363636', '#F75C95', '#ffb1e6', '#fff7ff' # color theme : darker to lighter

def ok(event):
    print("value is", var.get())

master = Tk()

var = StringVar(master)
var.set("one") # initial value

option = OptionMenu(master, var, "one", "two", "three", "four", command=ok)
option.configure(bg=COLOR1, fg=COLOR3, activebackground=COLOR1, activeforeground=COLOR3)
option["menu"].config(bg=COLOR1, fg=COLOR3, activebackground=COLOR1, activeforeground=COLOR4)
option.pack()

#
# test stuff



button = Button(master, text="OK", command=ok)
button.pack()

mainloop()