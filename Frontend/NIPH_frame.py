#!/usr/bin/env python3

import sys
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

import double_y_graphs

sys.path.append('../Backend') # appends the backend directory so we can use the modules there
from NIPH import NIPH_ILS_graf, NIPH_virus_detections

COLOR1, COLOR2, COLOR3, COLOR4 = '#363636', '#F75C95', '#ffb1e6', '#fff7ff' # color theme : darker to lighter
FIGURE_HEIGHT, TOOLBAR_HEIGHT = 310, 30

class NIPH_frame(Frame, Tk):
    def __init__(self, root):
        Frame.__init__(self, root, bg=COLOR4)
        
        self.graph_frame = Frame(self, bg='red', width=640, height=320)
        self.graph_frame.pack(side='bottom', fill='both', expand=True)

        NIPH_ili_figure = NIPH_ILS_graf.NIPH_ILI('../Backend/NIPH/ILI_tall_2016_17.xlsx').get_graph() # only season 16/17
        NIPH_virus_figure = NIPH_virus_detections.NIPH_Virus().get_graph()

        self.NIPH_ili_graph = self._plot_widget(self.graph_frame, NIPH_ili_figure)
        self.NIPH_virus_graph = self._plot_widget(self.graph_frame, NIPH_virus_figure)

        self.kolumbus_ili_graph = Frame()
        self.kolumbus_virus_graph = Frame()
        self.twitter_virus_graph = Frame()
        self.NPRA_ili_graph = Frame()
        self.NPRA_virus_graph = Frame()
        self.ruter_virus_graph = Frame()
        self.ruter_ili_graph = Frame()
        # default starting view
        #self.NIPH_ili_graph.pack(fill='both', expand=False)
        #self.IPH_virus_graph.pack(fill='both', expand=False)

        self.graphs = double_y_graphs.double_y_graph()
        
        # Possible permutations: 
        #self.kolumbus(2015, 2016)
        #self.kolumbus(2016, 2017)
        #self.ruter(2015, 2016)
        #self.ruter(2016, 2017)
        #self.ruter(2017, 2018)

        #self._toolbar(self)
        self._init_dropdowns()

    def _init_dropdowns(self):
        self.label = Label(self, text='Compare with: ', bg=COLOR4)
        self.label.pack(side='left')


        NPRA_items = (["Oslo", "15/16", "16/17"], ["Stavanger", "15/16", "16/17"],
                        ["Bergen", "15/16", "16/17"], ["All of Norway", "15/16", "16/17"])
        self._double_dropdown_menu(self, 'NPRA', NPRA_items)
        self._addButton(self, 'None')
        self._addButton(self, 'Twitter')
        kolumbus_items = ["15/16", "16/17"]
        self._single_dropdown_menu(self, 'Kolumbus', kolumbus_items)
        ruter_items = ["15/16", "16/17", "17/18"]
        self._single_dropdown_menu(self, 'Ruter', ruter_items)

    def ruter(self, start_year, end_year):
        self._forget_all_graphs()
        self._set_graph_season(start_year)
        if start_year == 2016:
            ruter_ili_figure = self.graphs._double_y_graph('ili', self.graphs.get_ruter_seasons_weekly(start_year, end_year))
            self.ruter_ili_graph = self._plot_widget(self.graph_frame, ruter_ili_figure)
            self.ruter_ili_graph.pack(fill='both', expand=False)
        ruter_virus_figure = self.graphs._double_y_graph('virus', self.graphs.get_ruter_seasons_weekly(start_year, end_year))
        self.ruter_virus_graph = self._plot_widget(self.graph_frame, ruter_virus_figure)
        self.ruter_virus_graph.pack(fill='both', expand=False)

    def NPRA(self, start_year, end_year, city):
        self._forget_all_graphs()
        self._set_graph_season(start_year)
        if start_year == 2016:
            NPRA_ili_figure = self.graphs._double_y_graph('ili', self.graphs.get_NPRA_seasons_weekly(start_year, end_year, city))
            self.NPRA_ili_graph = self._plot_widget(self.graph_frame, NPRA_ili_figure)
            self.NPRA_ili_graph.pack(fill='both', expand=False)
        NPRA_virus_figure = self.graphs._double_y_graph('virus', self.graphs.get_NPRA_seasons_weekly(start_year, end_year, city))
        self.NPRA_virus_graph = self._plot_widget(self.graph_frame, NPRA_virus_figure)
        self.NPRA_virus_graph.pack(fill='both', expand=False)

    def twitter(self):
        self._forget_all_graphs()
        self._set_graph_season(2017)
        twitter_virus_figure = self.graphs._double_y_graph('virus', self.graphs.get_twitter_seasons_weekly())
        self.twitter_virus_graph = self._plot_widget(self.graph_frame, twitter_virus_figure)
        self.twitter_virus_graph.pack(fill='both', expand=False)

    def kolumbus(self, start_year, end_year):
        self._forget_all_graphs()
        self._set_graph_season(start_year)
        if start_year == 2016:
            self.kolumbus_ili_figure = self.graphs._double_y_graph('ili', self.graphs.get_kolumbus_seasons_weekly(start_year, end_year))
            self.kolumbus_ili_graph = self._plot_widget(self.graph_frame, kolumbus_ili_figure)
            self.kolumbus_ili_graph.pack(fill='both', expand=False)

        self.kolumbus_virus_figure = self.graphs._double_y_graph('virus', self.graphs.get_kolumbus_seasons_weekly(start_year, end_year))
        self.kolumbus_virus_graph = self._plot_widget(self.graph_frame, kolumbus_virus_figure)
        self.kolumbus_virus_graph.pack(fill='both', expand=False)

    def NIPH(self):
        self._forget_all_graphs()
        self.NIPH_ili_graph.pack(fill='both', expand=False)
        self.NIPH_virus_graph.pack(fill='both', expand=False)

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

        figure_canvas = FigureCanvasTkAgg(figure, master=canvas)
        figure_canvas.get_tk_widget().pack(fill='both', expand=False)
        
        plot_widget = figure_canvas.get_tk_widget()
        plot_widget.configure(width=1, height=FIGURE_HEIGHT)

        toolbar = NavigationToolbar2TkAgg(figure_canvas, canvas)
        toolbar.pack(side=BOTTOM, fill=Y, expand=False)
        toolbar.configure(background=COLOR4)
        toolbar.update()

        return canvas

    def _toolbar(self, root):
        toolbar = Frame(root, bg=COLOR2)
        toolbar.pack(side='right', fill='both', expand=False)

        self.label = Label(root, text='Compare with: ', bg=COLOR4)
        self.label.pack(side='left')

        self._addButton(toolbar, "None")
        self._addButton(toolbar, "NPRA")
        self._addButton(toolbar, "Kolumbus")
        self._addButton(toolbar, "Ruter")
        self._addButton(toolbar, "Twitter")

        return toolbar

    def _buttonCallBack(self, name):
        if name == 'None': self.NIPH()
        elif name == 'Twitter': self.twitter()

    def _addButton(self, root, name):
        B = Button(root, text = name, width=10, bg=COLOR1, fg=COLOR3, bd=3,
            activebackground=COLOR1, activeforeground=COLOR3,
            command = lambda: self._buttonCallBack(name)
        )
        B.pack(side='left')
        return B

    def _single_dropdown_menu_callback(self, value):
        print('Value: ', value)

    def _single_dropdown_menu(self, root, name, items):
        #var = StringVar(root)
        #var.set(name) # initial value

        option = OptionMenu(root, name, *items, command=self._single_dropdown_menu_callback)
        option.configure(bg=COLOR1, fg=COLOR3, activebackground=COLOR1, activeforeground=COLOR3)
        option["menu"].config(bg=COLOR1, fg=COLOR3, activebackground=COLOR1, activeforeground=COLOR4)
        option.pack()

    def _double_dropdown_callback(self, value):
        if value[1] == '15/16': start_year, end_year = 2015, 2016
        elif value[1] == '16/17': start_year, end_year = 2016, 2017
        
        if value[0].lower() == 'all of norway': value[0] = 'Norway'
        self.NPRA(start_year, end_year, value[0])

    def _double_dropdown_menu(self, root, name, items):
        var = StringVar(value=name)
        menubutton = Menubutton(root, textvariable=var, indicatoron=True,
                                borderwidth=1, relief="raised", width=20,
                                bg=COLOR1, fg=COLOR3, activebackground=COLOR1, activeforeground=COLOR4)
        main_menu = Menu(menubutton, tearoff=False, bg=COLOR1, fg=COLOR3, activebackground=COLOR1, activeforeground=COLOR4)
        menubutton.configure(menu=main_menu)
        
        for item in range(len(items)):
            menu = Menu(main_menu, tearoff=False, bg=COLOR1, fg=COLOR3, activebackground=COLOR1, activeforeground=COLOR4)
            main_menu.add_cascade(label=items[item][0], menu=menu)
            for value in items[item][1:]:
                menu.add_radiobutton(value=value, label=value, variable=value,
                command= lambda item=item, value=value: self._double_dropdown_callback([items[item][0], value]))
        menubutton.pack()

def main():
    root = Tk()
    WINDOW_WIDTH, WINDOW_HEIGHT = 640, 640
    root.geometry("%dx%d" % (WINDOW_WIDTH, WINDOW_HEIGHT))
    root.wm_iconbitmap('sandra.ico')
    root.title("NIPH frame test")
    root.configure(background='green')
    
    frame = NIPH_frame(root)
    frame.pack()

    root.mainloop()

if __name__ == '__main__':
    main()