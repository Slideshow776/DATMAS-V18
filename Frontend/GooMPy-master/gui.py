# !/usr/bin/python3
from tkinter import *
from tkinter import messagebox
import sys, os
import matplotlib
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from openpyxl import load_workbook
import datetime

import ruter


def helloCallBack(message):
   # TODO: Vis alt som har med vegvesenet å gjøre
    print("Button " + message + " is ready.")

def addButton(frame, it, name, x, y, command):
    B = Button(frame, text = name, command = command, width = 10)
    B.place(x = x, y = y)
    B.grid(row=it, column=0)
    # B.pack(side=TOP)

def main():
    root = Tk()
    root.geometry("800x600")
    root.title("Masterappen, TODO: finn på et bedre navn")
    #root.rowconfigure(0, weight = 1)
    #vscrollbar = Scrollbar(root)
    #vscrollbar.pack(side=RIGHT, fill=Y)
    #hscrollbar = Scrollbar(root, orient='horizontal')
    #hscrollbar.pack(side=BOTTOM, fill=X)
    frame0 = Frame(root, bg='red')
    frame0.grid(row=0, column=0)

    addButton(frame0, 0, "Vegvesenet", 5, 5, helloCallBack("Vegvesenet"))
    addButton(frame0, 1, "FHI", 5, 35, helloCallBack("FHI"))
    addButton(frame0, 2, "Kolumbus", 5, 65, helloCallBack("Kolumbus"))
    addButton(frame0, 3, "Ruter", 5, 95, helloCallBack("Ruter"))
    addButton(frame0, 4, "Twitter", 5, 125, helloCallBack("Twitter"))

    frame1 = Frame(root, bg='yellow')
    frame1.grid(row=0, column=1)

    print("TEST: ", ruter)
    figure = ruter.get_graph()
    canvas1 = FigureCanvasTkAgg(figure, master=frame1)
    plot_widget1 = canvas1.get_tk_widget()
    plot_widget1.pack(side=RIGHT, fill=BOTH, expand=YES)

    frame2 = Frame(root, bg='green')
    frame2.grid(row=1, column=1)

    w = Canvas(frame2, width=640, height=640, bg="magenta")
    w.pack(side=LEFT, fill=BOTH, expand=YES)

    root.mainloop()

if __name__ == '__main__':
    main()
