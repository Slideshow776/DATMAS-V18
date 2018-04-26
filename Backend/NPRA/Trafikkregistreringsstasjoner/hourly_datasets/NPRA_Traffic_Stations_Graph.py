# coding=utf8

import sys, time, datetime
from openpyxl import load_workbook
import matplotlib.pyplot as plt, numpy as np

import NPRA_Traffic_Stations_load_data as NPRA_data

class NPRA_Traffic_Stations_load_graph:
    def __init__(self, filename):
        plt.tight_layout()
        self.year = 2017
        self._FIGURE = self.update_graph(self.year, filename, 1, 
                                        8, 9,   # hour_from, hour_to
                                        0, 4,   # weekday_from, weekday_to
                                        0, 3)   # month_from, month_to

    def update_graph(self, year, filename, field, hour_from, hour_to, # weeksdays range from 0-6, 0 is monday
         weekday_from, weekday_to, month_from, month_to):   # months range from 0-11, 0 is january
        self.year = year
        query_results = NPRA_data.query_data(year, filename, field, hour_from, hour_to, # weeksdays range from 0-6, 0 is monday
         weekday_from, weekday_to, month_from, month_to)
        self.title = query_results[0].get_id() + '' + str(year)
        return self._draw_graph(query_results)

    def _draw_graph(self, data):
        plt.figure(111)
        ticks, x, y = [], [], []
        for i in range(len(data)):
            ticks.append(data[i].get_date())
            x.append(i)
            y.append(data[i].get_vehicles())
        x = np.array(x)
        
        plt.plot(x, y)
        plt.xticks(x, ticks)
        plt.xticks(rotation=22.5)
        plt.title(self.title)
        plt.ylabel("Traffic per hour")
        #plt.legend(loc='upper left')
        plt.grid(axis='y', linestyle='-')
        plt.grid(axis='x', linestyle='-')
        figure = plt.figure(111)
        figure.patch.set_facecolor('#fff7ff')
        return figure
    
    def get_graph(self): return self._FIGURE

def main():
    NPRA_Traffic_Stations_load_graph(NPRA_data.HOURLY_FILE_NAME)
    plt.show()

if __name__ == '__main__':
    main()
