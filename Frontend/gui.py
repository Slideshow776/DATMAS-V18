# !/usr/bin/python3
from tkinter import *
from tkinter import messagebox
import sys, os
import matplotlib
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

sys.path.append('../Backend') # appends the backend directory so we can use the modules there

from Ruter import ruter
from FHI import FHI_ILS_graf, FHI_virus_detections
from Kolumbus import kolumbus
from NPRA import NPRA_weekly, NPRA_monthly
from Twitter import twitter_analyzer

import map_frame
import scrframe

WIDTH, HEIGHT = 1366, 768 # resolution of average laptop

def helloCallBack(name):
    print('Button was pressed: ', name)
    if name == 'FHI':
        FHI_ILI_graph.pack(fill='both', expand=True)
        ruter_graph.pack_forget()
    elif name == 'Ruter':
        FHI_ILI_graph.pack_forget()
        ruter_graph.pack(fill='both', expand=True)
    """elif name == 'Kolumbus':
    elif name == 'NPRA':
    elif name == 'Twitter':"""

def addButton(frame, name):
    B = Button(frame, text = name, command = lambda: helloCallBack(name), width = 10)
    B.pack(side=TOP, padx=2, pady=2)
    return B

def toolbar(root):
    toolbar = Frame(root, bg='cyan')
    toolbar.pack(side='left', fill='both', expand=False)

    addButton(toolbar, "NPRA")
    addButton(toolbar, "FHI")
    addButton(toolbar, "Kolumbus")
    addButton(toolbar, "Ruter")
    addButton(toolbar, "Twitter")

    return toolbar

def statusbar(root):
    status = Label(root, text="Idle...", bd=1, relief=SUNKEN, bg="yellow", anchor=W)
    status.grid(row = 3, column = 0, columnspan = 3, sticky='we')
    status.pack(side='bottom', fill=X, expand=True)
    status.place(anchor=N, x=root.winfo_height(), y=root.winfo_width()-20)

def scrollbar(container): # Jams a canvas inbetween which you can scroll on
    canvas = Canvas(container, bg='#cc99ff') # light purple
    frame = Frame(canvas, bg='#800000') # dark red
    scrollbar = Scrollbar(container, orient='vertical', command=canvas.yview)

    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side='right', fill='y', anchor='w')
    canvas.pack(fill='both', expand=True)
    canvas.create_window((200, 0), window=frame)
    frame.pack(fill='both', expand=True)
    frame.bind('<Configure>', lambda event: callback_scroll_function(event, canvas))
    return frame

def callback_scroll_function(event, canvas):
    canvas.configure(
        scrollregion=canvas.bbox("all"),
        width=695,
        height=HEIGHT
    )

def plot_widget(figure):
    figure_canvas = FigureCanvasTkAgg(figure, master=graph1)
    plot_widget = figure_canvas.get_tk_widget()
    plot_widget.pack(fill='both', expand=True)
    plot_widget.pack_forget()
    return plot_widget

root = Tk()
root.geometry("%dx%d" % (WIDTH, HEIGHT))
root.wm_iconbitmap('sandra.ico')
root.title("Automated collection of multi-source spatial information for emergency management")

container = Frame(root, bg='black', width=600, height=300)
container.pack(side="right", fill='both', expand=True)
#container.rowconfigure(0, weight = 1)
#container.columnconfigure(0, weight = 1)    

the_toolbar = toolbar(root)
#the_toolbar.focus_set()
#statusbar(root)

# ---------------- Dataframe -------------------------------------------
#data_frame = scrollbar(container)



#---------------
"""
data_frame = Canvas(
    container,
    bg ='#99ff99', # light green
    width=300,
    height=300,
    scrollregion=(0,0,500,500)
)

scrollbar = Scrollbar(container, orient='vertical')
scrollbar.pack(side=RIGHT, fill=Y)
scrollbar.config(command=data_frame.yview)

#data_frame.grid(row = 0, column = 1, sticky='nsew')
#data_frame.config(width=300, height=300)
data_frame.config(yscrollcommand=scrollbar.set)
data_frame.pack(fill='both', expand=True)
#data_frame.configure(scrollregion = data_frame.bbox("all"))
"""
#---------------

data_frame1 = scrframe.VerticalScrolledFrame(container)
data_frame1.pack(fill='both', expand=True)

graph1 = Frame(data_frame1.interior, bg='red')
graph1.pack(fill='both', expand=True)

figure_FHI_ILI = FHI_ILS_graf.FHI_ILI('../Backend/FHI/ILI_tall_2016_17.xlsx').get_graph()
figure_Ruter = ruter.Ruter('../Backend/Ruter/Antall påstigende per dag_Oslo_2015_2017.xlsx').get_graph()
"""figure_FHI_virus = 
figure_kolumbus = 
figure_twitter =""" 

FHI_ILI_graph = plot_widget(figure_FHI_ILI)
ruter_graph = plot_widget(figure_Ruter)

FHI_ILI_graph.pack(fill='both', expand=True)

#figure_canvas = FigureCanvasTkAgg(figure_FHI_ILI, master=graph1)
#plot_widget = figure_canvas.get_tk_widget()
#plot_widget.pack(fill='both', expand=True)

markers = []
markers.append([58.9362,5.5741])
markers.append([58.97,5.7331])
markers.append([58.939243,5.589634])

map_frame.Map(root, data_frame1.interior, markers) # creates a tkinter.Canvas

root.mainloop()
