# !/usr/bin/python3
from tkinter import *
from tkinter import messagebox
import sys, os
import matplotlib
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from openpyxl import load_workbook
import datetime

import cartopy.crs as ccrs
import cartopy.feature as cfeature
from example import UI

# current_dir = os.getcwd()
# root = os.path.dirname(current_dir) + r'\Ruter'
# sys.path.append(root)
# import Ruter

def isDate(date):
    try:
        datetime.datetime.strptime(date, '%d.%m.%Y')
        return True
    except ValueError:
        return False

def getData():
    workbook = load_workbook('Antall påstigende per dag_Oslo_2015_2017.xlsx')
    worksheet = workbook['Antall påstigende per dag_Oslo']
    
    years_dates, years_passengers = [], []
    dates, passengers = [], []
    for i in range(5, worksheet.max_row+1):
        if isDate(worksheet['A' + str(i)].value):
            dates.append(worksheet['A' + str(i)].value)
            passengers.append(worksheet['B' + str(i)].value)
        else:
            years_dates.append(dates)
            years_passengers.append(passengers)
            dates, passengers = [], []
    return years_dates, years_passengers

def drawGraph(dates, passengers):
    x_365 = []
    for i in range(365):
        x_365.append(i)
    x_365 = np.array(x_365)
    x_366 = []
    for i in range(366):
        x_366.append(i)
    x_366 = np.array(x_366)
    x_58 = []
    for i in range(58):
        x_58.append(i)
    x_58 = np.array(x_58)
    x_ticks = dates[0]

    y_2015 = passengers[0]
    y_2016 = passengers[1]
    y_2017 = passengers[2]
    y_2018 = passengers[3]

    plt.xticks(x_365, x_ticks)
    plt.xticks(rotation=45)
    plt.plot(x_365, y_2015, label="2015")
    plt.plot(x_366, y_2016, label="2016")
    plt.plot(x_365, y_2017, label="2017")
    plt.plot(x_58, y_2018, label="2018")

    plt.title('Passengers traveling with Ruter in Oslo county')
    plt.ylabel("Passengers")
    plt.legend(loc='upper left')
    plt.grid(axis='y', linestyle='-')
    plt.grid(axis='x', linestyle='-')
    #plt.show()
    return plt.figure(1)

def main():
    dates, passengers = getData()
    return drawGraph(dates, passengers)

top = Tk()
top.geometry("800x600")
top.title("Masterappen, TODO: finn på et bedre navn")
top.rowconfigure(0, weight = 1)

def helloCallBack(message):
   # TODO: Vis alt som har med vegvesenet å gjøre
    print("Button " + message + " is ready.")

def addButton(frame, it, name, x, y, command):
    B = Button(frame, text = name, command = command, width = 10)
    B.place(x = x, y = y)
    B.grid(row=it, column=0)
    # B.pack(side=TOP)

def drawMap():
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_extent([32, 3.928428, 71.894243, 57], crs=ccrs.PlateCarree())

    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAKES, alpha=0.5)
    ax.add_feature(cfeature.RIVERS)

    return fig

frame0 = Frame(top, bg='red')
frame0.grid(row=0, column=0)

addButton(frame0, 0, "Vegvesenet", 5, 5, helloCallBack("Vegvesenet"))
addButton(frame0, 1, "FHI", 5, 35, helloCallBack("FHI"))
addButton(frame0, 2, "Kolumbus", 5, 65, helloCallBack("Kolumbus"))
addButton(frame0, 3, "Ruter", 5, 95, helloCallBack("Ruter"))
addButton(frame0, 4, "Twitter", 5, 125, helloCallBack("Twitter"))

frame1 = Frame(top, bg='yellow')
frame1.grid(row=0, column=1)
frame1.rowconfigure(0, weight = 1)

figure = main()
canvas1 = FigureCanvasTkAgg(figure, master=frame1)
plot_widget1 = canvas1.get_tk_widget()
plot_widget1.grid(row=0, column=0)
# plot_widget1.place(x = 100, y = 5)
# plot_widget1.pack(side=RIGHT, fill=BOTH, expand=YES)

frame2 = Frame(top, bg='green')
frame2.grid(row=1, column=1)
frame2.rowconfigure(0, weight = 1)

figure2 = drawMap()

googlemap = UI()
canvas2 = googlemap.return_canvas()

#canvas2 = FigureCanvasTkAgg(figure2, master=frame2)
plot_widget2 = canvas2.get_tk_widget()
plot_widget2.grid(row=0, column=0)
# plot_widget.place(x = 200, y = 5)
# plot_widget2.pack(side=BOTTOM, fill=BOTH, expand=YES)

top.mainloop()
