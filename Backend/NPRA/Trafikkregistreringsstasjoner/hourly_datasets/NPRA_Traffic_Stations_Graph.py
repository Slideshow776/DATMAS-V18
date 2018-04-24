# coding=utf8

import sys
from openpyxl import load_workbook
import matplotlib.pyplot as plt, numpy as np

import NPRA_Traffic_Stations_load_data as NPRA_data

def main():
    field1, field2 = [], []
    """coordinates = NPRA_data.get_all_coordinates(
        NPRA_data.COORDINATES_STAVANGER_FILE_NAME,
        NPRA_data.COORDINATES_BERGEN_FILE_NAME,
        NPRA_data.COORDINATES_OSLO_FILE_NAME
    )"""
    for d in NPRA_data.get_data_hourly('2013',
        NPRA_data.HOURLY_FILE_NAME):
        if d.get_field() == 1: field1.append(d.get_all())
        #elif d.get_field() == 2: field2.append(d.get_all())
    draw_graph(field1)
    plt.show()

#def get_graph(): return _FIGURE

def draw_graph(data):        
        ticks, x, y = [], [], []
        for i in range(len(data)):
            ticks.append(data[i][0])
            x.append(i)
            y.append(data[i][3])
        x = np.array(x)
        
        plt.plot(x, y)
        plt.xticks(x, ticks)
        plt.xticks(rotation=45)
        plt.title('HILLEVÅGTUNNELEN 2013')
        plt.ylabel("Traffic per hour")
        #plt.legend(loc='upper left')
        plt.grid(axis='y', linestyle='-')
        plt.grid(axis='x', linestyle='-')
        figure = plt.figure()
        figure.patch.set_facecolor('#fff7ff')
        return figure

if __name__ == '__main__':
    main()
