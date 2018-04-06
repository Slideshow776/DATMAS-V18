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

import map_canvas
import scrframe

WIDTH, HEIGHT = 1366/1.2, 768/1.2 # resolution of average laptop

def helloCallBack(name):
    if name == 'FHI':
        FHI_ILI_graph.pack(fill='both', expand=True)
        FHI_virus_graph.pack(fill='both', expand=True)
        ruter_graph.pack_forget()
        kolumbus_graph.pack_forget()
        twitter_graph.pack_forget()
        NPRA_norway_graph.pack_forget()
        NPRA_bergen_graph.pack_forget()
        NPRA_stavanger_graph.pack_forget()
        NPRA_oslo_graph.pack_forget()
        map1.pack_forget()
    elif name == 'Ruter':
        FHI_ILI_graph.pack_forget()
        FHI_virus_graph.pack_forget()
        ruter_graph.pack(fill='both', expand=True)
        kolumbus_graph.pack_forget()
        twitter_graph.pack_forget()
        NPRA_norway_graph.pack_forget()
        NPRA_bergen_graph.pack_forget()
        NPRA_stavanger_graph.pack_forget()
        NPRA_oslo_graph.pack_forget()
        map1.pack_forget()
    elif name == 'Kolumbus':
        FHI_ILI_graph.pack_forget()
        FHI_virus_graph.pack_forget()
        ruter_graph.pack_forget()
        kolumbus_graph.pack(fill='both', expand=True)
        twitter_graph.pack_forget()
        NPRA_norway_graph.pack_forget()
        NPRA_bergen_graph.pack_forget()
        NPRA_stavanger_graph.pack_forget()
        NPRA_oslo_graph.pack_forget()
        map1.pack_forget()
    elif name == 'NPRA':
        FHI_ILI_graph.pack_forget()
        FHI_virus_graph.pack_forget()
        ruter_graph.pack_forget()
        kolumbus_graph.pack_forget()
        twitter_graph.pack_forget()
        NPRA_norway_graph.pack(fill='both', expand=True)
        NPRA_bergen_graph.pack(fill='both', expand=True)
        NPRA_stavanger_graph.pack(fill='both', expand=True)
        NPRA_oslo_graph.pack(fill='both', expand=True)
        map1.pack(fill='both', expand=True)
    elif name == 'Twitter':
        FHI_ILI_graph.pack_forget()
        FHI_virus_graph.pack_forget()
        ruter_graph.pack_forget()
        kolumbus_graph.pack_forget()
        twitter_graph.pack(fill='both', expand=True)
        NPRA_norway_graph.pack_forget()
        NPRA_bergen_graph.pack_forget()
        NPRA_stavanger_graph.pack_forget()
        NPRA_oslo_graph.pack_forget()
        map1.pack(fill='both', expand=True)

def addButton(frame, name):
    B = Button(
        frame,
        text = name,
        width=10,
        bg='#ffcfff',
        fg='#363636',
        bd=3,
        activebackground='#ffb1e6',
        activeforeground='#363636',
        highlightbackground='blue',
        highlightcolor='magenta',
        command = lambda: helloCallBack(name))
    B.pack(side=TOP, padx=2, pady=2)
    return B

def toolbar(root):
    toolbar = Frame(root, bg='#F75C95') # hello-kitty pink
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
    #plot_widget.pack(fill='both', expand=True)
    plot_widget.pack_forget()
    return plot_widget

print('Loading ... \n(this may take some seconds)')
root = Tk()
root.geometry("%dx%d" % (WIDTH, HEIGHT))
root.wm_iconbitmap('sandra.ico')
root.title("Automated collection of multi-source spatial information for emergency management")
root.configure(background='#363636')

container = Frame(root, bg='#363636', width=600, height=300)
container.pack(side="right", fill='both', expand=True)
#container.rowconfigure(0, weight = 1)
#container.columnconfigure(0, weight = 1)    

the_toolbar = toolbar(root)
#the_toolbar.focus_set()
#statusbar(root)

# ---------------- Dataframe -------------------------------------------
#data_frame = scrollbar(container)
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

data_frame1 = scrframe.VerticalScrolledFrame(container)
data_frame1.pack(fill='both', expand=True)

graph1 = Frame(data_frame1.interior, bg='#363636')
graph1.pack(fill='both', expand=True)

FHI_ILI_figure = FHI_ILS_graf.FHI_ILI('../Backend/FHI/ILI_tall_2016_17.xlsx').get_graph()
Ruter_figure = ruter.Ruter('../Backend/Ruter/Antall påstigende per dag_Oslo_2015_2017.xlsx').get_graph()
FHI_virus_figure = FHI_virus_detections.FHI_Virus().get_graph()
kolumbus_figure = kolumbus.Kolumbus().get_graph()
twitter_figure = twitter_analyzer.Twitter('../Backend/Twitter/twitter_data.txt').get_graph()
NPRA_stavanger_figure = NPRA_weekly.NPRA_weekly('../Backend/NPRA/Ukestrafikk 2013-2017 utvalgte punkter Bergen - Stavanger - Oslo.xlsx').get_specific_graph_('stavanger')
NPRA_norway_figure = NPRA_weekly.NPRA_weekly('../Backend/NPRA/Ukestrafikk 2013-2017 utvalgte punkter Bergen - Stavanger - Oslo.xlsx').get_specific_graph_('norway')
NPRA_bergen_figure = NPRA_weekly.NPRA_weekly('../Backend/NPRA/Ukestrafikk 2013-2017 utvalgte punkter Bergen - Stavanger - Oslo.xlsx').get_specific_graph_('bergen')
NPRA_oslo_figure = NPRA_weekly.NPRA_weekly('../Backend/NPRA/Ukestrafikk 2013-2017 utvalgte punkter Bergen - Stavanger - Oslo.xlsx').get_specific_graph_('oslo')

FHI_ILI_graph = plot_widget(FHI_ILI_figure)
ruter_graph = plot_widget(Ruter_figure)
FHI_virus_graph = plot_widget(FHI_virus_figure)
kolumbus_graph = plot_widget(kolumbus_figure)
twitter_graph = plot_widget(twitter_figure)
NPRA_stavanger_graph = plot_widget(NPRA_stavanger_figure)
NPRA_norway_graph = plot_widget(NPRA_norway_figure)
NPRA_bergen_graph = plot_widget(NPRA_bergen_figure)
NPRA_oslo_graph = plot_widget(NPRA_oslo_figure)

# default starting view
FHI_ILI_graph.pack(fill='both', expand=True)
FHI_virus_graph.pack(fill='both', expand=True)

#figure_canvas = FigureCanvasTkAgg(figure_FHI_ILI, master=graph1)
#plot_widget = figure_canvas.get_tk_widget()
#plot_widget.pack(fill='both', expand=True)

markers = []
markers.append([58.9362,5.5741])
markers.append([58.97,5.7331])
markers.append([58.939243,5.589634])

map1 = map_canvas.Map(root, data_frame1.interior, markers) # creates a tkinter.Canvas
map1.pack_forget()

print('Loading complete')
root.mainloop()
