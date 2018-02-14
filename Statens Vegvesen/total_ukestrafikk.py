# coding=utf8
"""
    Command lines: Enter a city of either Oslo, Bergen or Stavanger.
                   Then optionally enter weeks where you would like a vertical line to appear on the graph.
                   Commands are separated by a space.

    @ Sandra Moen
"""

import sys
from openpyxl import load_workbook
import matplotlib.pyplot as plt
import numpy as np

print("Accepts command lines first: [Bergen, Oslo or Stavanger] second: set of vertical lines in weeks")
if not sys.argv[1:]:
    print("Error: please insert city name!")
if len(sys.argv) >= 2:
    vertical_lines = []
    for i in range(2, len(sys.argv)):
        vertical_lines.append(int(sys.argv[i]))
user_input_places = sys.argv[1:][0].lower()
if not user_input_places == 'oslo' and not user_input_places == 'bergen' and not user_input_places == 'stavanger':
    print("Error: Invalid command, please choose from 'Oslo' or 'Bergen'")

wb2 = load_workbook(r'C:\Users\Slideshow\Dropbox\School\DATMAS-V18\Git\Statens Vegvesen\Ukestrafikk 2013-2017 utvalgte punkter Bergen - Stavanger - Oslo.xlsx')
if user_input_places == 'bergen':
    ws = wb2['Bergen']
elif user_input_places == 'oslo':
    ws = wb2['Oslo']
elif user_input_places == 'stavanger':
    ws = wb2['Stavanger']

def getData(year):    
    weeks = []
    for i in range(0, 52):
        weeks.append(0)

    for i in range(13, ws.max_row):
        if ws['A' + str(i)].value == year:        
            for j in range(0, len(weeks)):
                if j < 25: # xlm counts A-Z, then AA-AZ ...
                    if not isinstance(ws[chr(66+j) + str(i)].value, int): # chr(66) = B in ascii
                        continue
                    weeks[j] += int(ws[chr(66+j) + str(i)].value)
                elif j < 51:
                    if not isinstance(ws[chr(65) + chr(65+j-25) + str(i)].value, int): # chr(66) = B in ascii
                        continue
                    weeks[j] += int(ws[chr(65) + chr(65+j-25) + str(i)].value)
                else:
                    if not isinstance(ws[chr(66) + chr(65) + str(i)].value, int): # chr(66) = B in ascii
                        continue
                    weeks[j] += int(ws[chr(66) + chr(65) + str(i)].value)


    return weeks

def drawGraph(data):
    ticks, x = [], []
    for i in range(0, 52):
        ticks.append("Uke " + str(i+1))
        x.append(i)
    x = np.array(x)

    colors=["#FF0000", "#800000", "#FFFF00", "#808000", "#00FF00", "#008000", "#00FFFF", "#008080", "#0000FF", "#000080", "#FF00FF", "#800080", "#f58231", "#aaffc3"]
    for i in range(2, len(data)+2):
        y = np.array(data[i-2])
        label = "201" + str(i+1)
        plt.plot(x, y, label=label, color=colors[i-2])

    

    plt.xticks(x, ticks)
    plt.xticks(rotation=45)
    plt.title('Ukestrafikk fra Statens Vegvesen 2002-2015 i ' + user_input_places.title())
    plt.ylabel("Trafikk per uke")
    plt.legend(loc='upper left')
    plt.grid(axis='y', linestyle='-')
    plt.grid(axis='x', linestyle='-')
    for xc in vertical_lines:
        plt.axvline(x=xc, color='magenta', linestyle='--')
    plt.show()

data_years = []
for i in range(2013, 2018): # data tilgjengelig år 2013-2017
    data_years.append(getData(i))
drawGraph(data_years)