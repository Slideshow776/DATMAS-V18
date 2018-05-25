import sys
from tkinter import filedialog
from tkinter import *
import matplotlib.pyplot as plt
sys.path.append('../Backend') # appends the backend directory so we can use the modules there
sys.path.append('../Backend/NPRA/Trafikkregistreringsstasjoner/hourly_datasets')
import map_canvas, NPRA_Traffic_Stations_load_data, NPRA_Traffic_Stations_Graph
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import constants

BUTTON_WIDTH, BUTTON_HEIGHT, BORDERWIDTH = 12, 0, 3
FIGURE_HEIGHT, TOOLBAR_HEIGHT = 610, 30

class NPRA_frame(Frame, Tk):
    def __init__(self, root, width, height):

        Frame.__init__(self, root, bg=constants.COLOR_THEME[3])

        self.graph_frame = Frame(self, width=int(width*(2/3)), height=height, bg='#ff9900') # orange
        self.graph_frame.pack(side='right', fill='both', expand=True)

        # Controls
        self.control_frame = Frame(self.graph_frame, bg=constants.COLOR_THEME[3])
        self.control_frame.pack(side='top', fill='x', expand=False)        
        self._hours_frame(self.control_frame, 1, 1)
        self._weekdays_frame(self.control_frame, 1, 2)
        self._months_frame(self.control_frame, 1, 3)
        
        show_btn = Button(self.control_frame, text='Show', command=self._show_btn_callback,
            bg=constants.COLOR_THEME[0], fg=constants.COLOR_THEME[2], activebackground=constants.COLOR_THEME[0], activeforeground=constants.COLOR_THEME[3])
        self._radio_buttons_init(self.control_frame)
        show_btn.grid(row=1, column=5)
        
        save_btn = Button(self.control_frame, text='Save', command=self._save_btn_callback,
            bg=constants.COLOR_THEME[0], fg=constants.COLOR_THEME[2], activebackground=constants.COLOR_THEME[0], activeforeground=constants.COLOR_THEME[3])
        save_btn.grid(row=1, column=6)
        
        self.v = StringVar()
        self.v.set('')
        self.error = Label(self.control_frame, textvariable=self.v, bg=constants.COLOR_THEME[3], fg='#ff0000', width=15, padx=10)
        self.error.grid(row=1, column=7) # red

        # Graph
        self.filename = '../Backend/NPRA/Trafikkregistreringsstasjoner/hourly_datasets/Stavanger/1100009 HILLEVÅGTUNNELEN 2013-2017.xlsx'
        self.years = [2017]
        self.NPRA_traffic_Station = NPRA_Traffic_Stations_Graph.NPRA_Traffic_Stations_load_graph(self.filename, self.years)
        self.graph_figure = self.NPRA_traffic_Station.get_graph()
        self.graph_graph = self._plot_widget(self.graph_frame, self.graph_figure)
        self.graph_graph.pack(side='bottom', fill='both', expand=True)

        # Map
        coordinates = NPRA_Traffic_Stations_load_data.get_all_coordinates(
            '../Backend/NPRA/Trafikkregistreringsstasjoner/hourly_datasets/Stavanger/times nivå 1 STAVANGER.csv',
            '../Backend/NPRA/Trafikkregistreringsstasjoner/hourly_datasets/Bergen/times nivå 1 BERGEN.csv',
            '../Backend/NPRA/Trafikkregistreringsstasjoner/hourly_datasets/Oslo/times nivå 1 OSLO.csv',
            )
        self.map1 = map_canvas.Map(self, width=int(width*(1/3)), height=height, coordinates=coordinates) #coordinates)
        self.map1.pack(side='left', expand=False)
        
        self.query_data = []
        self.years = [2017]

    def _radio_buttons_init(self, root):
        frame = Frame(root, bg='#ff6a22')
        years = [2017, 2016, 2015, 2014, 2013]
        for year in years:
            check_button = Checkbutton(frame, text=year, variable=year, bg=constants.COLOR_THEME[0], fg=constants.COLOR_THEME[2],
                selectcolor='#121212', activebackground=constants.COLOR_THEME[0], activeforeground=constants.COLOR_THEME[2], #black-grey
                command=lambda year=year: self._checkbox_callback(year))
            check_button.pack()#check_button.grid(row=2018-year, column=4)
            if year == 2017: check_button.select()
        frame.grid(row=1, column=4)
    
    def _plot_widget(self, root, figure):
        canvas = Canvas(root, background=constants.COLOR_THEME[3])
        
        figure_canvas = FigureCanvasTkAgg(figure, master=canvas)
        figure_canvas.get_tk_widget().pack(side='bottom', fill='both', expand=True)

        toolbar = NavigationToolbar2TkAgg(figure_canvas, canvas)
        toolbar.pack(side='top', fill=Y, expand=False)
        toolbar.configure(background=constants.COLOR_THEME[3])
        toolbar.update()
            
        return canvas

    def _months_frame(self, root, row=1, column=1):
        months_frame = Frame(root, bg=constants.COLOR_THEME[3])
        months = 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'
        self._single_dropdown_menu(months_frame, 'Month from', months, 1, 1)
        self.months_from_var = StringVar()
        self.months_from_var.set('January')
        self.months_from = Label(months_frame, bg=constants.COLOR_THEME[3], textvariable=self.months_from_var)
        self.months_from.grid(row=2, column=1)
        self._single_dropdown_menu(months_frame, 'Month to', months, 1, 2)
        self.months_to_var = StringVar()
        self.months_to_var.set('March')
        self.months_to = Label(months_frame, bg=constants.COLOR_THEME[3], textvariable=self.months_to_var)
        self.months_to.grid(row=2, column=2)
        months_frame.grid(row=row, column=column)

    def _weekdays_frame(self, root, row=1, column=1):
        weekdays_frame = Frame(root, bg=constants.COLOR_THEME[3])
        weekdays = 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
        self._single_dropdown_menu(weekdays_frame, 'Weekday from', weekdays, 1, 1)
        self.weekdays_from_var = StringVar()
        self.weekdays_from_var.set('Monday')
        self.weekdays_from = Label(weekdays_frame, bg=constants.COLOR_THEME[3], textvariable=self.weekdays_from_var)
        self.weekdays_from.grid(row=2, column=1)
        self._single_dropdown_menu(weekdays_frame, 'Weekday to', weekdays, 1, 2)
        self.weekdays_to_var = StringVar()
        self.weekdays_to_var.set('Friday')
        self.weekdays_to = Label(weekdays_frame, bg=constants.COLOR_THEME[3], textvariable=self.weekdays_to_var)
        self.weekdays_to.grid(row=2, column=2)
        weekdays_frame.grid(row=row, column=column)

    def _hours_frame(self, root, row=1, column=1):
        hours_frame = Frame(root, bg=constants.COLOR_THEME[3])
        hours = '00', '01', '02', '03', '04', '05', '06', '07', '08', '09', 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 21, 22, 23
        self._single_dropdown_menu(hours_frame, 'Hours from', hours, 1, 1)
        self.hours_from_var = StringVar()
        self.hours_from_var.set('08')
        self.hours_from = Label(hours_frame, bg=constants.COLOR_THEME[3], textvariable=self.hours_from_var)
        self.hours_from.grid(row=2, column=1)
        self._single_dropdown_menu(hours_frame, 'Hours to', hours, 1, 2)
        self.hours_to_var = StringVar()
        self.hours_to_var.set('09')
        self.hours_to = Label(hours_frame, bg=constants.COLOR_THEME[3], textvariable=self.hours_to_var)
        self.hours_to.grid(row=2, column=2)
        hours_frame.grid(row=row, column=column)
    
    def _convert_weekday_to_number(self, weekday):
        if weekday.lower() == 'monday': return 0
        elif weekday.lower() == 'tuesday': return 1
        elif weekday.lower() == 'wednesday': return 2
        elif weekday.lower() == 'thursday': return 3
        elif weekday.lower() == 'friday': return 4
        elif weekday.lower() == 'saturday': return 5
        elif weekday.lower() == 'sunday': return 6

    def _convert_month_to_number(self, month):
        if month.lower() == 'january': return 0
        elif month.lower() == 'february': return 1
        elif month.lower() == 'march': return 2
        elif month.lower() == 'april': return 3
        elif month.lower() == 'may': return 4
        elif month.lower() == 'june': return 5
        elif month.lower() == 'july': return 6
        elif month.lower() == 'august': return 7
        elif month.lower() == 'september': return 8
        elif month.lower() == 'october': return 9
        elif month.lower() == 'november': return 10
        elif month.lower() == 'december': return 11

    def _checkbox_callback(self, year):
        if year in self.years: self.years.remove(year)
        else: self.years.append(year)

    def _save_btn_callback(self):
        save_to_url =  filedialog.asksaveasfilename(
            initialdir = "/", title = "Save As", filetypes = (("csv files","*.csv"),("all files","*.*"))
        )
        save_to_url += '.csv'
        f = open(save_to_url, "w")
        f.write('year,month,day,hour,vehicles\n')
        for i in range(len(self.query_data)): # for how many years there are
            for j in range(len(self.query_data[i])): # for how many items in that year
                f.write(
                    str(self.query_data[i][j][0])+','+
                    str(self.query_data[i][j][1])+','+
                    str(self.query_data[i][j][2])+','+
                    str(self.query_data[i][j][3])+','+
                    str(self.query_data[i][j][4])+'\n'
                )

    def _show_btn_callback(self):
        hour_from, hour_to = int(self.hours_from_var.get()), int(self.hours_to_var.get())
        weekday_from, weekday_to = self._convert_weekday_to_number(self.weekdays_from_var.get()), self._convert_weekday_to_number(self.weekdays_to_var.get())
        month_from, month_to = self._convert_month_to_number(self.months_from_var.get()), self._convert_month_to_number(self.months_to_var.get())
        #specs = [hour_from, hour_to, weekday_from, weekday_to, month_from, month_to]
        #print(specs)
        if (hour_from > hour_to or weekday_from > weekday_to or month_from > month_to or not self.years): 
            self.error.configure(fg='red')
            self.v.set('Error, invalid request!')
            return
        self.error.configure(fg='orange')
        self.v.set('Loading, please wait ...')
        self.control_frame.update_idletasks()

        plt.gcf().clear()
        self.graph_graph.pack_forget()
        self.graph_graph = None
        self.graph_figure = None
        self.NPRA_traffic_Station.clear_graph()
        self.query_data = []
        for year in self.years:
            self.graph_figure, temp = self.NPRA_traffic_Station.update_graph(year, self.filename, 1, hour_from, hour_to, weekday_from, weekday_to, month_from, month_to)
            self.query_data.append(temp)
        self.graph_graph = self._plot_widget(self.graph_frame, self.graph_figure)
        self.graph_graph.pack(side='bottom', fill='both', expand=True)        
        self.v.set('')

    def _single_dropdown_menu_callback(self, value):
        if value[0] == 'Hours from': self.hours_from_var.set(value[1])
        elif value[0] == 'Hours to': self.hours_to_var.set(value[1])
        elif value[0] == 'Weekday from': self.weekdays_from_var.set(value[1])
        elif value[0] == 'Weekday to': self.weekdays_to_var.set(value[1])
        elif value[0] == 'Month from': self.months_from_var.set(value[1])
        elif value[0] == 'Month to': self.months_to_var.set(value[1])

    def _single_dropdown_menu(self, root, name, items, row=1, column=1):
            var = StringVar()
            menubutton = Menubutton(root, text=name, borderwidth=BORDERWIDTH, relief="raised", indicatoron=False, bg=constants.COLOR_THEME[0],
                            fg=constants.COLOR_THEME[2], activebackground=constants.COLOR_THEME[0], activeforeground=constants.COLOR_THEME[3], width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
            menu = Menu(menubutton, tearoff=False, bg=constants.COLOR_THEME[0], fg=constants.COLOR_THEME[2], activebackground=constants.COLOR_THEME[0], activeforeground=constants.COLOR_THEME[3])
            menubutton.configure(menu=menu)
            for item in items:
                menu.add_radiobutton(label=item, variable=var, value=item,
                command= lambda item=item: self._single_dropdown_menu_callback([name, item]))
            menubutton.grid(row=row, column=column)

    def get_frame(self): return self.graph_frame
    def get_map_label(self): return self.map1.winfo_children()[0]
    def get_map(self): return self.map1

def main():
    root = Tk()
    WINDOW_WIDTH, WINDOW_HEIGHT = int(1366/1.2), int(768/1.2) # (1366, 768) is the resolution of an average laptop.
    root.geometry("%dx%d" % (WINDOW_WIDTH, WINDOW_HEIGHT))
    root.wm_iconbitmap('sandra.ico')
    root.title("NPRA frame test")
    root.configure(background='#000000') # black
    
    NPRA_frame(root, WINDOW_WIDTH, WINDOW_HEIGHT).pack(expand=True, fill='both')
    
    root.mainloop()

if __name__ == '__main__':
    main()