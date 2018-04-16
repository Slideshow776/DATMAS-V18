# coding=utf8

import sys
from openpyxl import load_workbook
import matplotlib.pyplot as plt, numpy as np

import NPRA_Traffic_Stations_load_data as NPRA_data

def main():
    field1, field2 = [], []
    for d in NPRA_data.get_data('2013'):
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

        colors=["#FF0000", "#800000", "#FFFF00", "#808000", "#00FF00", "#008000", "#00FFFF", "#008080", "#0000FF", "#000080", "#FF00FF", "#800080", "#f58231", "#aaffc3"]
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
