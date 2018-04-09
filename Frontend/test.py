# !/usr/bin/python3
from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk 
import sys, os, time, threading
import matplotlib
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


root2 = Tk()
root2.overrideredirect(True)
#root2.geometry("%dx%d" % (WIDTH/2, HEIGHT/2))
root2.geometry('+%d+%d'%(60, 60))
root2.configure(background='magenta')
progressbar = ttk.Progressbar(master=root2, orient=HORIZONTAL, length=100, mode='indeterminate', maximum=10)
progressbar.pack()
progressbar.start()

root2.mainloop()