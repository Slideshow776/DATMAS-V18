# !/usr/bin/python3
from tkinter import *
from tkinter import messagebox
import sys, os
import matplotlib
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import ruter
import example

def helloCallBack():
    print("helloCallBack: TODO")

def addButton(frame, name, command):
    B = Button(frame, text = name, command = command, width = 10)
    B.pack(side=TOP, padx=2, pady=2)

def main():
    root = Tk()
    root.geometry("800x600")
    root.wm_iconbitmap('sandra.ico')
    root.title("Automated collection of multi-source spatial information for emergency management")

    container = Frame(root)
    container.pack(side="right", fill='both', expand=True)
    container.rowconfigure(0, weight = 1)
    container.columnconfigure(0, weight = 1)

    # ---------------- Toolbar ---------------------------------------------
    toolbar = Frame(root, bg='cyan', width=100)
    toolbar.pack(side='left', fill='both', expand=False)
    """
    toolbar.grid(rowspan = 3, sticky='ns')
    toolbar.columnconfigure(0, weight=2)
    toolbar.rowconfigure(0, weight=2)
    toolbar.grid_propagate(False)
    toolbar.grid_propagate(False)
    """

    addButton(toolbar, "Vegvesenet", helloCallBack)
    addButton(toolbar, "FHI", helloCallBack)
    addButton(toolbar, "Kolumbus", helloCallBack)
    addButton(toolbar, "Ruter", helloCallBack)
    addButton(toolbar, "Twitter", helloCallBack)

    # ---------------- Dataframe -------------------------------------------
    data_frame = Frame(container, bg ='black')
    #data_frame.grid(row = 0, column = 1, sticky='nsew')
    data_frame.pack()
    
    # ----------------------------------------------------------------------
    graph1 = Frame(data_frame, bg='red')
    graph1.pack(side=TOP, fill='both', expand=True)
    
    ruterFigure = ruter.Ruter(1)
    figure = ruterFigure.get_graph()

    canvas1 = FigureCanvasTkAgg(figure, master=graph1)
    plot_widget1 = canvas1.get_tk_widget()
    plot_widget1.pack(side=RIGHT, fill=BOTH, expand=True)
    """
    # ----------------------------------------------------------------------
    the_map = example.Map(data_frame)
    map1 = the_map.get_frame() #Frame(data_frame, bg='green')
    #map1.pack(side=BOTTOM) #, fill='both', expand=True)
    #w = the_map.get_frame()
    #w.pack()
    #w = Canvas(map1, width=640, height=80, bg="magenta")
    #w.pack(side=LEFT, fill=BOTH, expand=True)

    # ---------------- Status bar ------------------------------------------
    #status = Label(root, text="Idle...", bd=1, relief=SUNKEN, bg="yellow", anchor=W)
    #status.grid(row = 3, column = 0, columnspan = 3, sticky='we')
    #status.pack(side='bottom', fill=X, expand=True)
    #status.place(anchor=N, x=root.winfo_height(), y=root.winfo_width()-20)

    root.mainloop()

if __name__ == '__main__':
    main()
