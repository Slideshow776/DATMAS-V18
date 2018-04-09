import tkinter as tk

def change_color():
    root.configure(background='blue')

root = tk.Tk()
root.configure(background='red')
root.after(2000, change_color) # 'after' uses milliseconds, so 1,000 = 1 second
root.mainloop()