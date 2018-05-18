#!/usr/bin/env python3

"""
    @author: Sandra Moen
    Bug: Does heavy re-calculations, store these instead (longest load is ~49 seconds)
"""

import sys
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

import double_y_graphs

sys.path.append('../Backend') # appends the backend directory so we can use the modules there
from NIPH import NIPH_ILS_graf, NIPH_virus_detections

COLOR1, COLOR2, COLOR3, COLOR4 = '#363636', '#F75C95', '#ffb1e6', '#fff7ff' # color theme : darker to lighter
BUTTON_WIDTH, BUTTON_HEIGHT, BORDERWIDTH = 10, 0, 3
FIGURE_HEIGHT, TOOLBAR_HEIGHT = 581, 30

class NIPH_frame(Frame, Tk):
    def __init__(self, root):
        self.pixel = PhotoImage(width=1, height=2) # mad hack to force pixel sizing, this makes the buttons appear with same width and height
        
        Frame.__init__(self, root, bg=COLOR4)
        self.button_frame = Frame(self, bg=COLOR4)
        self.button_frame.pack(side='top', fill='x', expand=False)
        self.graph_frame = Frame(self, bg=COLOR4)
        self.graph_frame.pack(fill='both', expand=False)

        NIPH_ili_figure = NIPH_ILS_graf.NIPH_ILI('../Backend/NIPH/ILI_tall_2016_17.xlsx').get_graph() # only season 16/17
        NIPH_virus_figure = NIPH_virus_detections.NIPH_Virus(False).get_graph()

        self.NIPH_ili_graph = self._plot_widget(self.graph_frame, NIPH_ili_figure)
        self.NIPH_virus_graph = self._plot_widget(self.graph_frame, NIPH_virus_figure)

        self.kolumbus_ili_figure = None
        self.NPRA_ili_figure = None

        self.kolumbus_ili_graph = Frame()
        self.kolumbus_virus_graph = Frame()
        self.twitter_virus_graph = Frame()
        self.NPRA_ili_graph = Frame()
        self.NPRA_virus_graph = Frame()
        self.ruter_virus_graph = Frame()
        self.ruter_ili_graph = Frame()
        
        self.graphs = double_y_graphs.double_y_graph()
        self._init_dropdowns()

        self.v = StringVar()
        self.label = Label(self.button_frame, textvariable=self.v, fg='orange', bg=COLOR4).pack(side='left')
        self.v.set('')
        self.label_isVisible = False
    
    def _toggle_label(self):
        if self.label_isVisible:
            self.v.set('')
            self.label_isVisible = False
        else:
            self.v.set('Loading, please wait ...')
            self.label_isVisible = True

    def _init_dropdowns(self):
        self.label = Label(self.button_frame, text='Compare with: ', bg=COLOR4)
        self.label.pack(side='left')
        self._addButton(self.button_frame, 'None')       
        NPRA_items = (["Oslo", "15/16", "16/17"], ["Stavanger", "15/16", "16/17"],
                        ["Bergen", "15/16", "16/17"], ["All of Norway", "15/16", "16/17"])
        self._double_dropdown_menu(self.button_frame, 'NPRA', NPRA_items)        
        kolumbus_items = ["15/16", "16/17"]
        self._single_dropdown_menu(self.button_frame, 'Kolumbus', kolumbus_items)        
        ruter_items = ["15/16", "16/17", "17/18"]
        self._single_dropdown_menu(self.button_frame, 'Ruter', ruter_items)
        self._addButton(self.button_frame, 'Twitter')

    def _ruter(self, start_year, end_year):
        self._forget_all_graphs()
        self._set_graph_season(start_year)
        if start_year == 2016:
            ruter_ili_figure = self.graphs._double_y_graph('ili', self.graphs.get_ruter_seasons_weekly(start_year, end_year), 'NIPH ILI', 'RUTER')
            self.ruter_ili_graph = self._plot_widget(self.graph_frame, ruter_ili_figure)
            self.ruter_ili_graph.pack(fill='both', expand=True)
        ruter_virus_figure = self.graphs._double_y_graph('virus', self.graphs.get_ruter_seasons_weekly(start_year, end_year), 'NIPH Virus', 'RUTER')
        self.ruter_virus_graph = self._plot_widget(self.graph_frame, ruter_virus_figure)
        self.ruter_virus_graph.pack(fill='both', expand=True)

    def _NPRA(self, start_year, end_year, city):
        self._forget_all_graphs()
        self._set_graph_season(start_year)
        if start_year == 2016:
            if not self.NPRA_ili_figure:
                self.NPRA_ili_figure = self.graphs._double_y_graph('ili', self.graphs.get_NPRA_seasons_weekly(start_year, end_year, city), 'NIPH ILI', 'NPRA')
                self.NPRA_ili_graph = self._plot_widget(self.graph_frame, self.NPRA_ili_figure)
            self.NPRA_ili_graph.pack(fill='both', expand=True)
        NPRA_virus_figure = self.graphs._double_y_graph('virus', self.graphs.get_NPRA_seasons_weekly(start_year, end_year, city), 'NIPH Virus', 'NPRA')
        self.NPRA_virus_graph = self._plot_widget(self.graph_frame, NPRA_virus_figure)
        self.NPRA_virus_graph.pack(fill='both', expand=True)

    def _twitter(self):
        self._forget_all_graphs()
        self._set_graph_season(2017)
        twitter_virus_figure = self.graphs._double_y_graph('virus', self.graphs.get_twitter_seasons_weekly(), 'NIPH Virus', 'Twitter')
        self.twitter_virus_graph = self._plot_widget(self.graph_frame, twitter_virus_figure)
        self.twitter_virus_graph.pack(fill='both', expand=True)

    def _kolumbus(self, start_year, end_year):
        self._forget_all_graphs()
        self._set_graph_season(start_year)
        if start_year == 2016:
            if not self.kolumbus_ili_figure:
                self.kolumbus_ili_figure = self.graphs._double_y_graph('ili', self.graphs.get_kolumbus_seasons_weekly(start_year, end_year), 'NIPH ILI', 'Kolumbus')
                self.kolumbus_ili_graph = self._plot_widget(self.graph_frame, self.kolumbus_ili_figure)
            self.kolumbus_ili_graph.pack(fill='both', expand=True)

        self.kolumbus_virus_figure = self.graphs._double_y_graph('virus', self.graphs.get_kolumbus_seasons_weekly(start_year, end_year), 'NIPH Virus', 'Kolumbus')
        self.kolumbus_virus_graph = self._plot_widget(self.graph_frame, self.kolumbus_virus_figure)
        self.kolumbus_virus_graph.pack(fill='both', expand=True)

    def _NIPH(self):
        self._forget_all_graphs()
        self.NIPH_ili_graph.pack(fill='both', expand=True)
        self.NIPH_virus_graph.pack(fill='both', expand=True)

    def _forget_all_graphs(self):
        self.kolumbus_ili_graph.pack_forget()
        self.kolumbus_virus_graph.pack_forget()
        self.twitter_virus_graph.pack_forget()
        self.NPRA_ili_graph.pack_forget()
        self.NPRA_virus_graph.pack_forget()
        self.ruter_virus_graph.pack_forget()
        self.ruter_ili_graph.pack_forget()
        self.NIPH_ili_graph.pack_forget()
        self.NIPH_virus_graph.pack_forget()

    def _set_graph_season(self, start_year):
        if start_year == 2015: self.graphs.set_season('15/16')
        elif start_year == 2016: self.graphs.set_season('16/17')
        elif start_year == 2017: self.graphs.set_season('17/18')

    def _plot_widget(self, root, figure):
        canvas = Canvas(root, background=COLOR4) 
        canvas.configure(height=FIGURE_HEIGHT + TOOLBAR_HEIGHT) # height is to ameliorate the flickering bug
        canvas.pack(fill='both', expand=False)

        figure_canvas = FigureCanvasTkAgg(figure, master=canvas)
        figure_canvas.get_tk_widget().pack(fill='both', expand=False)
        
        plot_widget = figure_canvas.get_tk_widget()
        plot_widget.configure(width=1, height=FIGURE_HEIGHT)

        toolbar = NavigationToolbar2TkAgg(figure_canvas, canvas)
        toolbar.pack(side=BOTTOM, fill=Y, expand=False)
        toolbar.configure(background=COLOR4)
        toolbar.update()

        return canvas

    def _buttonCallBack(self, name):
        self._toggle_label()
        self.button_frame.update_idletasks()
        if name == 'None': self._NIPH()
        elif name == 'Twitter': self._twitter()
        self._toggle_label()

    def _addButton(self, root, name):
        B = Button(root, text = name, image=self.pixel, width=68, height=21, bg=COLOR1, fg=COLOR3, bd=BORDERWIDTH,
            activebackground=COLOR1, activeforeground=COLOR3, compound="c", padx=0, pady=0,
            command = lambda: self._buttonCallBack(name)
        )
        B.pack(side='left')
        return B

    def _value_check(self, value):
        if value[1] == '15/16': start_year, end_year = 2015, 2016
        elif value[1] == '16/17': start_year, end_year = 2016, 2017
        elif value[1] == '17/18': start_year, end_year = 2017, 2018
        return start_year, end_year

    def _single_dropdown_menu_callback(self, value):
        self._toggle_label()
        self.button_frame.update_idletasks()
        start_year, end_year = self._value_check(value)
        if value[0] == 'Ruter': self._ruter(start_year, end_year)
        elif value[0] == 'Kolumbus': self._kolumbus(start_year, end_year)
        self._toggle_label()

    def _single_dropdown_menu(self, root, name, items):
        var = StringVar()
        menubutton = Menubutton(root, text=name, borderwidth=BORDERWIDTH, relief="raised", indicatoron=False, bg=COLOR1,
                        fg=COLOR3, activebackground=COLOR1, activeforeground=COLOR4, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
        menu = Menu(menubutton, tearoff=False, bg=COLOR1, fg=COLOR3, activebackground=COLOR1, activeforeground=COLOR4)
        menubutton.configure(menu=menu)
        for item in items:
            menu.add_radiobutton(label=item, variable=var, value=item,
            command= lambda item=item: self._single_dropdown_menu_callback([name, item]))
        menubutton.pack(side='left')

    def _double_dropdown_callback(self, value):
        self._toggle_label()
        self.button_frame.update_idletasks()
        start_year, end_year = self._value_check(value)
        if value[0].lower() == 'all of norway': value[0] = 'Norway'
        self._NPRA(start_year, end_year, value[0])
        self._toggle_label()

    def _double_dropdown_menu(self, root, name, items):
        var = StringVar(value=name)
        menubutton = Menubutton(root, textvariable=var, indicatoron=False, borderwidth=BORDERWIDTH, relief="raised",
                        bg=COLOR1, fg=COLOR3, activebackground=COLOR1, activeforeground=COLOR4, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
        main_menu = Menu(menubutton, tearoff=False, bg=COLOR1, fg=COLOR3, activebackground=COLOR1, activeforeground=COLOR4)
        menubutton.configure(menu=main_menu)
        
        for item in range(len(items)):
            menu = Menu(main_menu, tearoff=False, bg=COLOR1, fg=COLOR3, activebackground=COLOR1, activeforeground=COLOR4)
            main_menu.add_cascade(label=items[item][0], menu=menu)
            for value in items[item][1:]:
                menu.add_radiobutton(value=value, label=value, variable=value,
                command= lambda item=item, value=value: self._double_dropdown_callback([items[item][0], value]))
        menubutton.pack(side='left')

def main():
    root = Tk()
    WINDOW_WIDTH, WINDOW_HEIGHT = int(1366/1.2), int(768/1.2) # (1366, 768) is the resolution of an average laptop.
    root.geometry("%dx%d" % (WINDOW_WIDTH, WINDOW_HEIGHT))
    root.wm_iconbitmap('sandra.ico')
    root.title("NIPH frame test")
    root.configure(background='#000000')
    
    frame = NIPH_frame(root)
    frame.pack(fill='both', expand=True)

    root.mainloop()

if __name__ == '__main__':
    main()