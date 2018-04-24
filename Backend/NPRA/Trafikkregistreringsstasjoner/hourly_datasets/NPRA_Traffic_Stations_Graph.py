# coding=utf8

import sys, time, datetime
from openpyxl import load_workbook
import matplotlib.pyplot as plt, numpy as np

import NPRA_Traffic_Stations_load_data as NPRA_data

class NPRA_Traffic_Stations_load_graph:
    def __init__(self, filename):
        self._FIGURE = self.set_data('2013', filename, 1,
                                        8, 9,   # hour_from, hour_to
                                        0, 4,   # weekday_from, weekday_to
                                        0, 3)  # month_from, month_to

    def set_data(self, year, filename, field, hour_from, hour_to, # weeksdays range from 0-6, 0 is monday
         weekday_from, weekday_to, month_from, month_to):   # months range from 0-11, 0 is january
        data = NPRA_data.get_data_hourly(year, filename)
        query_results = []
        for d in data:
            if (
                d.get_field() == field and
                hour_from <= d.get_date().hour <= hour_to and
                weekday_from <= d.get_date().weekday() <= weekday_to and
                month_from <= d.get_date().month <= month_to
            ) : query_results.append(d.get_all())
        return self._draw_graph(query_results)

    def _draw_graph(self, data):
        plt.figure(111)
        ticks, x, y = [], [], []
        for i in range(len(data)):
            ticks.append(data[i][1]) # 1 is place of date
            x.append(i)
            y.append(data[i][3]) # 3 is place of vehicles
        x = np.array(x)
        
        plt.plot(x, y)
        plt.xticks(x, ticks)
        plt.xticks(rotation=45)
        plt.title('HILLEVÅGTUNNELEN 2013')
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
