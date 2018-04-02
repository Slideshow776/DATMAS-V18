import tkinter as tk
class MYapp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        container.rowconfigure(0, weight = 1)
        container.columnconfigure(0, weight = 1)
        self.frames = {}
        for FRAME in (N1, N2):
            frame = FRAME(container, self)
            self.frames[FRAME] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")
            frame.rowconfigure(0, weight = 1)
            frame.columnconfigure(0, weight = 1)
            frame.columnconfigure(1, weight = 1)
        self.show_frame(N1)
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
class N1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        a = tk.Button(self, text = "N1", command = lambda: controller.show_frame(N2))
        a.grid(row = 0, column = 0, sticky = "nsew")
        c = tk.Button(self, text = "N1", command = lambda: controller.show_frame(N2))
        c.grid(row = 0, column = 1, sticky = "nsew")
class N2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        b = tk.Button(self, text = "N2")
        b.grid(row = 0, column = 0, sticky = "nsew")
if __name__ == "__main__":
    app = MYapp()
    app.mainloop()