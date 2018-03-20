import sys
import os

if sys.version_info[0] < 3:
    import Tkinter as tk
    import ttk as ttk
else:
    import tkinter as tk
    import tkinter.ttk as ttk

#
# LeftMiddle
#
class LeftMiddle(tk.Frame):
    def __init__(self, master=None):
        self.parent = master
        tk.Frame.__init__(self, self.parent, bg='bisque', borderwidth=1, relief="sunken")
        self.__create_layout()
        self.draw_text()

    def __create_layout(self):
        self.canvas = tk.Canvas(self, bg="green", relief=tk.SUNKEN)
        self.canvas.config(width=20, height=10)
        self.canvas.config(highlightthickness=0)

        self.sbar = tk.Scrollbar(self, orient=tk.VERTICAL)

        self.sbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, expand="YES", fill=tk.BOTH)

    def draw_text(self):    
        self.canvas.create_text(0, 0, text='1234567890', fill='red')
        self.canvas.create_text(0, 25, text='ABCDEFGH', fill='blue')

#
# MainWindow
#
class MainWindow(tk.Frame):
    def __init__(self, master=None):
        self.parent = master
        tk.Frame.__init__(self, self.parent, bg='bisque', borderwidth=1, relief="sunken")
        self.__create_layout()

    def __create_layout(self):
        self.frame1 = tk.Frame(self, bg="yellow")
        self.frame2 = tk.Frame(self, bg="blue")
        self.frame3 = LeftMiddle(self)  # tk.Frame(self, bg="green")
        self.frame4 = tk.Frame(self, bg="brown")
        self.frame5 = tk.Frame(self, bg="pink")

        self.frame1.grid(row=0, column=0, rowspan=4, columnspan=8, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.frame2.grid(row=0, column=8, rowspan=4, columnspan=2, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.frame3.grid(row=4, column=0, rowspan=2, columnspan=5, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.frame4.grid(row=4, column=5, rowspan=2, columnspan=5, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.frame5.grid(row=5, column=0, rowspan=1, columnspan=10, sticky=(tk.N, tk.S, tk.W, tk.E))

        for r in range(6):
            self.rowconfigure(r, weight=1)
        for c in range(10):
            self.columnconfigure(c, weight=1)
#
#   MAIN
#
def main():
    root = tk.Tk()

    root.title("Frames")
    root.geometry("550x300+525+300")

    root.configure(background="#808080")
    root.option_add("*font", ("Courier New", 9, "normal"))

    window = MainWindow(master=root)
    window.pack(side="top", fill="both", expand=True)
    root.mainloop()

if __name__ == '__main__':
    main()