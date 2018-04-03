# !/usr/bin/python3
from tkinter import *
from tkinter import messagebox
import sys, os
import matplotlib
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import ruter
import map_frame

WIDTH, HEIGHT = 800, 600


def helloCallBack():
    print("helloCallBack: TODO")

def addButton(frame, name, command):
    B = Button(frame, text = name, command = command, width = 10)
    B.pack(side=TOP, padx=2, pady=2)
    return B

def toolbar(root):
    toolbar = Frame(root, bg='cyan')
    toolbar.pack(side='left', fill='both', expand=False)

    addButton(toolbar, "Vegvesenet", helloCallBack)
    addButton(toolbar, "FHI", helloCallBack)
    addButton(toolbar, "Kolumbus", helloCallBack)
    addButton(toolbar, "Ruter", helloCallBack)
    addButton(toolbar, "Twitter", helloCallBack)

    return toolbar

def statusbar(root):
    status = Label(root, text="Idle...", bd=1, relief=SUNKEN, bg="yellow", anchor=W)
    status.grid(row = 3, column = 0, columnspan = 3, sticky='we')
    status.pack(side='bottom', fill=X, expand=True)
    status.place(anchor=N, x=root.winfo_height(), y=root.winfo_width()-20)

def scroll_function(event, canvas):
    canvas.configure(
        scrollregion=canvas.bbox("all"),
        width=695,
        height=HEIGHT
    )

def click(event):
    print("gui.py: ", event.x, event.y)

def main():
    root = Tk()
    root.geometry("%dx%d" % (WIDTH, HEIGHT))
    root.wm_iconbitmap('sandra.ico')
    root.title("Automated collection of multi-source spatial information for emergency management")

    container = Frame(root)
    container.pack(side="right", fill='both', expand=True)
    container.rowconfigure(0, weight = 1)
    container.columnconfigure(0, weight = 1)    

    the_toolbar = toolbar(root)
    #the_toolbar.focus_set()
    #statusbar(root)

    canvas = Canvas(container)
    frame = Frame(canvas)
    scrollbar = Scrollbar(container, orient='vertical', command=canvas.yview)

    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side='right', fill='y')
    canvas.pack()
    canvas.create_window((200, 0), window=frame, anchor='nw')
    frame.bind('<Configure>', lambda event: scroll_function(event, canvas))

    # ---------------- Dataframe -------------------------------------------
    data_frame = Frame(frame, bg ='black')
    #data_frame.grid(row = 0, column = 1, sticky='nsew')
    data_frame.pack()
    
    
    graph1 = Frame(data_frame, bg='red', width=640, height=160)
    graph1.pack(side=TOP, fill='both', expand=True)
    
    figure = ruter.Ruter().get_graph()

    canvas1 = FigureCanvasTkAgg(figure, master=graph1)
    plot_widget1 = canvas1.get_tk_widget()
    plot_widget1.pack(side=RIGHT, fill=BOTH, expand=True)
    
    markers = []
    markers.append([58.9362,5.5741])
    markers.append([58.97,5.7331])
    markers.append([58.939243,5.589634])

    map_frame.Map(root, data_frame, markers)
    
    root.mainloop()

if __name__ == '__main__':
    main()
