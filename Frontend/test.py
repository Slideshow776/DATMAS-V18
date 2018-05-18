from tkinter import filedialog
from tkinter import *
 
root = Tk()
filename =  filedialog.asksaveasfilename(
    initialdir = "/", title = "Save As", filetypes = (("csv files","*.csv"),("all files","*.*"))
)
print (filename)