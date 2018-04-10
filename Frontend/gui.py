# !/usr/bin/python3
from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk 
import sys, os, time, threading
import matplotlib
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

sys.path.append('../Backend') # appends the backend directory so we can use the modules there

from Ruter import ruter
from NIPH import NIPH_ILS_graf, NIPH_virus_detections
from Kolumbus import kolumbus
from NPRA import NPRA_weekly, NPRA_monthly
from Twitter import twitter_analyzer

import map_canvas
import scrframe

NIPH_ILI_graph = None
ruter_graph = None
NIPH_virus_graph = None
kolumbus_graph = None
twitter_graph = None
NPRA_stavanger_graph = None
NPRA_norway_graph = None
NPRA_bergen_graph = None
NPRA_oslo_graph = None
map1 = None
progress_var = None
theLabel = None
progressbar = None

WINDOW_WIDTH, WINDOW_HEIGHT = 1366/1.2, 768/1.2 # (1366, 768) is the resolution of an average laptop.
FIGURE_HEIGHT, TOOLBAR_HEIGHT = 610, 30
COLOR1, COLOR2, COLOR3, COLOR4 = '#363636', '#F75C95', '#ffb1e6', '#fff7ff' # color theme : darker to lighter

def helloCallBack(name):
    NIPH_ILI_graph.pack_forget()
    NIPH_virus_graph.pack_forget()
    ruter_graph.pack_forget()
    kolumbus_graph.pack_forget()
    twitter_graph.pack_forget()
    NPRA_norway_graph.pack_forget()
    NPRA_bergen_graph.pack_forget()
    NPRA_stavanger_graph.pack_forget()
    NPRA_oslo_graph.pack_forget()
    map1.pack_forget()
    if name == 'NIPH':
        NIPH_ILI_graph.pack(fill='both', expand=True)
        NIPH_virus_graph.pack(fill='both', expand=True)
    elif name == 'Ruter':
        ruter_graph.pack(fill='both', expand=True)
    elif name == 'Kolumbus':
        kolumbus_graph.pack(fill='both', expand=True)
    elif name == 'NPRA':
        NPRA_norway_graph.pack(fill='both', expand=True)
        NPRA_bergen_graph.pack(fill='both', expand=True)
        NPRA_stavanger_graph.pack(fill='both', expand=True)
        NPRA_oslo_graph.pack(fill='both', expand=True)
        map1.pack(fill='both', expand=True)
    elif name == 'Twitter':
        twitter_graph.pack(fill='both', expand=True)
        map1.pack(fill='both', expand=True)

def addButton(frame, name):
    B = Button(
        frame,
        text = name,
        width=10,
        bg=COLOR3,
        fg=COLOR1,
        bd=3,
        activebackground=COLOR3,
        activeforeground=COLOR1,
        highlightbackground='blue',
        highlightcolor='magenta',
        command = lambda: helloCallBack(name))
    B.pack(side=TOP, padx=2, pady=2)
    return B

def toolbar(root):
    toolbar = Frame(root, bg=COLOR2) # hello-kitty pink
    toolbar.pack(side='left', fill='both', expand=False)

    addButton(toolbar, "NPRA")
    addButton(toolbar, "NIPH")
    addButton(toolbar, "Kolumbus")
    addButton(toolbar, "Ruter")
    addButton(toolbar, "Twitter")

    return toolbar

def statusbar(root):
    status = Label(root, text="Idle...", bd=1, relief=SUNKEN, bg="white", anchor=W)
    status.pack(side=BOTTOM, fill=X, expand=False)
    #status.place(anchor=S, x=200, y=200)

def plot_widget(root, figure):
    canvas = Canvas(root, background=COLOR4) # height is to ameliorate the flickering bug
    canvas.configure(height=FIGURE_HEIGHT + TOOLBAR_HEIGHT)
    #canvas.pack(fill='both', expand=True)
    #canvas.pack_forget()
    
    figure_canvas = FigureCanvasTkAgg(figure, master=canvas)
    figure_canvas.get_tk_widget().pack(fill='both', expand=False)
    
    plot_widget = figure_canvas.get_tk_widget()
    plot_widget.configure(width=1, height=FIGURE_HEIGHT)

    toolbar = NavigationToolbar2TkAgg(figure_canvas, canvas)
    toolbar.pack(side=BOTTOM, fill=Y, expand=False)
    toolbar.configure(background=COLOR4)
    toolbar.update()
        
    return canvas

def progress_bar(root):
    global progress_var
    global theLabel
    global progressbar
    
    PROGRESS_MAX, progress_var = 9, DoubleVar()
    theLabel = Label(
        anchor=S,
        master=root,
        text="LOADING",
        height=int(WINDOW_HEIGHT/32),
        background=COLOR1,
        foreground=COLOR2
    )
    theLabel.pack(side=TOP)

    style = ttk.Style() 
    style.theme_use('default') 
    style.configure("black.Horizontal.TProgressbar", background=COLOR3)
    progressbar = ttk.Progressbar(
        root,
        variable=progress_var,
        maximum=PROGRESS_MAX,
        style='black.Horizontal.TProgressbar'
    )
    progressbar.pack()

root = Tk()
root.geometry("%dx%d" % (WINDOW_WIDTH, WINDOW_HEIGHT))
root.wm_iconbitmap('sandra.ico')
root.title("Automated collection of multi-source spatial information for emergency management")
root.configure(background=COLOR1)

container = Frame(root, bg=COLOR1)
container.pack(side="right", fill='both', expand=True)

the_toolbar = toolbar(root)
#statusbar(container)
progress_bar(container)

"""
self.canvas = Canvas(...)
self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
...
def _on_mousewheel(self, event):
    self.canvas.yview_scroll(-1*(event.delta/120), "units")
"""

def data_frame1():
    # ---------------- Dataframe -------------------------------------------
    data_frame1 = scrframe.VerticalScrolledFrame(container)

    graph1 = Frame(data_frame1.interior, bg=COLOR1)
    graph1.pack(fill='both', expand=True)
 
    global progress_var
    global theLabel
    global progressbar

    progress_var.set(0)
    root.update_idletasks()
    NIPH_ILI_figure = NIPH_ILS_graf.NIPH_ILI('../Backend/NIPH/ILI_tall_2016_17.xlsx').get_graph()
    progress_var.set(1)
    root.update_idletasks()
    NIPH_virus_figure = NIPH_virus_detections.NIPH_Virus().get_graph()
    """progress_var.set(2)
    root.update_idletasks()
    Ruter_figure = ruter.Ruter('../Backend/Ruter/Antall påstigende per dag_Oslo_2015_2017.xlsx').get_graph()
    progress_var.set(3)
    root.update_idletasks()
    kolumbus_figure = kolumbus.Kolumbus().get_graph()
    progress_var.set(4)
    root.update_idletasks()
    twitter_figure = twitter_analyzer.Twitter('../Backend/Twitter/twitter_data.txt').get_graph()
    progress_var.set(5)
    root.update_idletasks()
    NPRA_stavanger_figure = NPRA_weekly.NPRA_weekly('../Backend/NPRA/Ukestrafikk 2013-2017 utvalgte punkter Bergen - Stavanger - Oslo.xlsx').get_specific_graph_('stavanger')
    progress_var.set(6)
    root.update_idletasks()
    NPRA_norway_figure = NPRA_weekly.NPRA_weekly('../Backend/NPRA/Ukestrafikk 2013-2017 utvalgte punkter Bergen - Stavanger - Oslo.xlsx').get_specific_graph_('norway')
    progress_var.set(7)
    root.update_idletasks()
    NPRA_bergen_figure = NPRA_weekly.NPRA_weekly('../Backend/NPRA/Ukestrafikk 2013-2017 utvalgte punkter Bergen - Stavanger - Oslo.xlsx').get_specific_graph_('bergen')
    progress_var.set(8)
    root.update_idletasks()
    NPRA_oslo_figure = NPRA_weekly.NPRA_weekly('../Backend/NPRA/Ukestrafikk 2013-2017 utvalgte punkter Bergen - Stavanger - Oslo.xlsx').get_specific_graph_('oslo')
    progress_var.set(9)
    root.update_idletasks()"""

    global NIPH_ILI_graph
    NIPH_ILI_graph = plot_widget(graph1, NIPH_ILI_figure)
    global NIPH_virus_graph
    NIPH_virus_graph = plot_widget(graph1, NIPH_virus_figure)
    """global ruter_graph
    ruter_graph = plot_widget(graph1, Ruter_figure)
    global kolumbus_graph
    kolumbus_graph = plot_widget(graph1, kolumbus_figure)
    global twitter_graph
    twitter_graph = plot_widget(graph1, twitter_figure)
    global NPRA_stavanger_graph
    NPRA_stavanger_graph = plot_widget(graph1, NPRA_stavanger_figure)
    global NPRA_norway_graph
    NPRA_norway_graph = plot_widget(graph1, NPRA_norway_figure)
    global NPRA_bergen_graph
    NPRA_bergen_graph = plot_widget(graph1, NPRA_bergen_figure)
    global NPRA_oslo_graph
    NPRA_oslo_graph = plot_widget(graph1, NPRA_oslo_figure)"""

    # default starting view
    NIPH_ILI_graph.pack(fill='both', expand=False)
    NIPH_virus_graph.pack(fill='both', expand=False)

    markers = []
    markers.append([58.9362,5.5741])
    markers.append([58.97,5.7331])
    markers.append([58.939243,5.589634])

    global map1
    map1 = map_canvas.Map(root, data_frame1.interior, markers) # creates a tkinter.Canvas
    map1.pack_forget()
    
    theLabel.pack_forget()
    progressbar.pack_forget()
    data_frame1.pack(side=TOP, fill='both', expand=True)

root.after(1, data_frame1) # a little hack to make the window load properly before the other widgets

root.mainloop()
