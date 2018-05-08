# !/usr/bin/python3
import sys, os, time

from tkinter import *
import tkinter.ttk as ttk 

import matplotlib, numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

import map_canvas, scrframe, NIPH_frame, NPRA_frame

sys.path.append('../Backend') # appends the backend directory so we can use the modules there
sys.path.append('../Backend/NPRA/Trafikkregistreringsstasjoner/hourly_datasets')

from Ruter import ruter
from NIPH import NIPH_ILS_graf, NIPH_virus_detections
from Kolumbus import kolumbus
from NPRA import NPRA_weekly, NPRA_monthly
from Twitter import twitter_analyzer
import NPRA_Traffic_Stations_load_data

WINDOW_WIDTH, WINDOW_HEIGHT = int(1366/1.2), int(768/1.2) # (1366, 768) is the resolution of an average laptop.
FIGURE_HEIGHT, TOOLBAR_HEIGHT = 610, 30
COLOR1, COLOR2, COLOR3, COLOR4 = '#363636', '#F75C95', '#ffb1e6', '#fff7ff' # color theme : darker to lighter

the_map = None
#data_frame1 = None

def toolbarCallBack(name):
    #NIPH_ILI_graph.pack_forget()
    #NIPH_virus_graph.pack_forget()
    ruter_graph.pack_forget()
    kolumbus_graph.pack_forget()
    twitter_graph.pack_forget()
    NPRA_norway_graph.pack_forget()
    NPRA_bergen_graph.pack_forget()
    NPRA_stavanger_graph.pack_forget()
    NPRA_oslo_graph.pack_forget()
    map1.pack_forget()
    NIPH_frame1.pack_forget()
    NPRA_frame1.pack_forget()
    if name == 'NIPH':
        NIPH_frame1.pack(fill='both', expand=True)
        #NIPH_ILI_graph.pack(fill='both', expand=True)
        #NIPH_virus_graph.pack(fill='both', expand=True)
    elif name == 'Ruter':
        ruter_graph.pack(fill='both', expand=True)
    elif name == 'Kolumbus':
        kolumbus_graph.pack(fill='both', expand=True)
    elif name == 'NPRA':
        NPRA_frame1.pack(fill='both', expand=True)
        NPRA_norway_graph.pack(fill='both', expand=True)
        NPRA_bergen_graph.pack(fill='both', expand=True)
        NPRA_stavanger_graph.pack(fill='both', expand=True)
        NPRA_oslo_graph.pack(fill='both', expand=True)
        map1.pack(fill='both', expand=True)
    elif name == 'Twitter':
        twitter_graph.pack(fill='both', expand=True)
        map1.pack(fill='both', expand=True)

def addButton(frame, name):
    B = Button(frame, text = name, width=10, bg=COLOR3, fg=COLOR1, bd=3,
        activebackground=COLOR3, activeforeground=COLOR1, 
        command = lambda: toolbarCallBack(name)
    )
    B.pack(side=TOP, padx=2, pady=2)
    return B

def toolbar(root):
    toolbar = Frame(root, bg=COLOR2)
    toolbar.pack(side='left', fill='both', expand=False)

    addButton(toolbar, "NPRA")
    addButton(toolbar, "NIPH")
    addButton(toolbar, "Kolumbus")
    addButton(toolbar, "Ruter")
    addButton(toolbar, "Twitter")

    return toolbar

def plot_widget(root, figure):
    canvas = Canvas(root, background=COLOR4) 
    canvas.configure(height=FIGURE_HEIGHT + TOOLBAR_HEIGHT) # height is to ameliorate the flickering bug
    
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

def poll_for_focus_between_map_and_graphs(root):
    global data_frame1, the_map, map1, data_frame1
    x,y = root.winfo_pointerxy()
    widget = root.winfo_containing(x,y)
    if widget:
        if widget == the_map: map1.set_focus_here()
        else: data_frame1.set_focus_here()
    root.after(200, poll_for_focus_between_map_and_graphs, root)

def load_matplotlib_figures():
    graph1 = Frame(data_frame1.interior, bg=COLOR1)
    graph1.focus_set()
    graph1.pack(fill='both', expand=True)

    global progress_var, theLabel, progressbar, NIPH_frame1, NPRA_frame1
    
    NIPH_frame1 = NIPH_frame.NIPH_frame(graph1)
    progress_var.set(0)
    root.update_idletasks()
    #NIPH_ILI_figure = NIPH_ILS_graf.NIPH_ILI('../Backend/NIPH/ILI_tall_2016_17.xlsx').get_graph()
    #progress_var.set(1)
    #root.update_idletasks()
    #NIPH_virus_figure = NIPH_virus_detections.NIPH_Virus().get_graph()
    progress_var.set(1)
    root.update_idletasks()
    Ruter_figure = ruter.Ruter('../Backend/Ruter/Antall påstigende per dag_Oslo_2015_2017.xlsx').get_graph()
    progress_var.set(2)
    root.update_idletasks()
    kolumbus_figure = kolumbus.Kolumbus().get_graph()
    progress_var.set(3)
    root.update_idletasks()
    twitter_figure = twitter_analyzer.Twitter('../Backend/Twitter/twitter_data.txt').get_graph()
    progress_var.set(4)
    root.update_idletasks()
    NPRA_frame1 = NPRA_frame.NPRA_frame(graph1, WINDOW_WIDTH, WINDOW_HEIGHT)
    NPRA_frame1.pack_forget()
    progress_var.set(5)
    root.update_idletasks()
    NPRA_norway_figure = NPRA_weekly.NPRA_weekly('../Backend/NPRA/Ukestrafikk 2013-2017 utvalgte punkter Bergen - Stavanger - Oslo.xlsx').get_specific_graph_('norway')
    progress_var.set(6)
    root.update_idletasks()
    NPRA_bergen_figure = NPRA_weekly.NPRA_weekly('../Backend/NPRA/Ukestrafikk 2013-2017 utvalgte punkter Bergen - Stavanger - Oslo.xlsx').get_specific_graph_('bergen')
    progress_var.set(7)
    root.update_idletasks()
    NPRA_oslo_figure = NPRA_weekly.NPRA_weekly('../Backend/NPRA/Ukestrafikk 2013-2017 utvalgte punkter Bergen - Stavanger - Oslo.xlsx').get_specific_graph_('oslo')
    progress_var.set(8)
    root.update_idletasks()
    NPRA_stavanger_figure = NPRA_weekly.NPRA_weekly('../Backend/NPRA/Ukestrafikk 2013-2017 utvalgte punkter Bergen - Stavanger - Oslo.xlsx').get_specific_graph_('stavanger')
    progress_var.set(9)
    root.update_idletasks()  

    global NIPH_ILI_graph, NIPH_virus_graph, ruter_graph, kolumbus_graph, twitter_graph, NPRA_stavanger_graph, NPRA_norway_graph, NPRA_bergen_graph, NPRA_oslo_graph
    ruter_graph = plot_widget(graph1, Ruter_figure)
    kolumbus_graph = plot_widget(graph1, kolumbus_figure)
    twitter_graph = plot_widget(graph1, twitter_figure)
    NPRA_stavanger_graph = plot_widget(graph1, NPRA_stavanger_figure)
    NPRA_norway_graph = plot_widget(graph1, NPRA_norway_figure)
    NPRA_bergen_graph = plot_widget(graph1, NPRA_bergen_figure)
    NPRA_oslo_graph = plot_widget(graph1, NPRA_oslo_figure)

    # default starting view
    NIPH_frame1.pack(fill='both', expand=True)

def load_map():
    coordinates = NPRA_Traffic_Stations_load_data.get_all_coordinates(
        '../Backend/NPRA/Trafikkregistreringsstasjoner/hourly_datasets/Stavanger/times nivå 1 STAVANGER.csv',
        '../Backend/NPRA/Trafikkregistreringsstasjoner/hourly_datasets/Bergen/times nivå 1 BERGEN.csv',
        '../Backend/NPRA/Trafikkregistreringsstasjoner/hourly_datasets/Oslo/times nivå 1 OSLO.csv',
        )

    global map1
    map1 = map_canvas.Map(data_frame1.interior, coordinates, WINDOW_WIDTH, WINDOW_HEIGHT) # creates a tkinter.Canvas
    #map1.pack(fill='both', expand=True)
    map1.pack_forget()

def data_frame1():
    # ---------------- Dataframe -------------------------------------------
    global data_frame1
    data_frame1 = scrframe.VerticalScrolledFrame(container)

    load_matplotlib_figures()   
    theLabel.pack_forget()
    progressbar.pack_forget()
    data_frame1.pack(side=TOP, fill='both', expand=True)
    
    load_map()

    global graphs, the_map # used for polling the scrollbar focus
    graphs = data_frame1.winfo_children()[1].winfo_children()[0].winfo_children()[0].winfo_children()[0].winfo_children()[0]
    the_map = map1.winfo_children()[0]

root = Tk()
root.geometry("%dx%d" % (WINDOW_WIDTH, WINDOW_HEIGHT))
root.wm_iconbitmap('sandra.ico')
root.title("Automated collection of multi-source spatial information for emergency management")
root.configure(background=COLOR1)

#poll_for_focus_between_map_and_graphs(root)

container = Frame(root, bg=COLOR1)
container.pack(side="right", fill='both', expand=True)

the_toolbar = toolbar(root)
progress_bar(container)

root.after(1, data_frame1) # a little hack to make the window load properly before the data_frame1 widget
root.mainloop()
