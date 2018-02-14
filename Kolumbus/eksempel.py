import csv
import matplotlib.pyplot as plt
import numpy as np

def load_data():
    scv_to_read = r'C:\Users\Slideshow\Dropbox\School\DATMAS-V18\Fra Erlend\PER_DAYsoldticketsbytype_2015-06-01_2015-07-31.csv'

    # Read CSV file
    with open(scv_to_read, 'r') as fp:
        reader = csv.reader(fp, delimiter=';')
        next(reader, None)  # skip the headers
        data_read = [row for row in reader]
    return data_read

def totalt(data):
    x, y = [], []
    tempx, tempy = '', 0
    for d in data:
        if tempx != d[0]:
            x.append(d[0])
            tempx = d[0]

    for i in range(0, len(x)):
        for j in range(0, len(data)):
            if x[i] == data[j][0]:
                tempy += int(data[j][1])
        y.append(tempy)
        tempy = 0
    return x, y

def daglig(data):
    x, y = [], []
    tempx, tempy = '', 0
    for d in data:
        if tempx != d[0]:
            x.append(d[0])
            tempx = d[0]
    
    acceptable = ['Voksen',
                    'Barn',
                    'Sykkel',
                    'Honnør',
                    'Dagspass Voksen',
                    'Dagspass Barn',
                    'Dagspass Honnør',
                    '1 dag voksen',
                    '1 dag barn',
                    '1 dag honnør',
                    '3 dager voksen',
                    '3 dager barn',
                    '3 dager honnør'
                    'Voksen Enkelt Ferge', 
                    'Voksen Enkel Hurtigbåt',
                    'Barn Enkelt Ferge', 
                    'Barn Enkel Hurtigbåt',
                    'Honnør Enkelt Ferge', 
                    'Honnør Enkel Hurtigbåt',
          ]
    for i in range(0, len(x)):
        for j in range(0, len(data)):
            if x[i] == data[j][0] and data[j][2] in acceptable:
                tempy += int(data[j][1])
        y.append(tempy)
        tempy = 0
    return x, y


def periode(data):
    x, y = [], []
    tempx, tempy = '', 0
    for d in data:
        if tempx != d[0]:
            x.append(d[0])
            tempx = d[0]
    
    acceptable = ['7 dager voksen',
                    '14 dager voksen',
                    '30 dager voksen',
                    '7 dager barn',
                    '14 dager barn',
                    '30 dager barn',
                    '7 dager honnør',
                    '14 dager honnør',
                    '30 dager honnør',
                    '7 dager ungdom',
                    '14 dager ungdom',
                    '30 dager ungdom',
                    '7 dager student',
                    '14 dager student',
                    '30 dager student',
                    'Voksen Periode Hurtigbåt',
                    'Barn Periode Hurtigbåt',
                    'Honnør Periode Hurtigbåt',
                    'Ungdom Periode Hurtigbåt',
                    'Student Periode Hurtigbåt',
                    'Voksen Periode Ferge',
                    'Barn Periode Ferge',
                    'Honnør Periode Ferge',
                    'Ungdom Periode Ferge',
                    'Student Periode Ferge',
          ]
    for i in range(0, len(x)):
        for j in range(0, len(data)):
            if x[i] == data[j][0] and data[j][2] in acceptable:
                tempy += int(data[j][1])
        y.append(tempy)
        tempy = 0
    return x, y

def draw_line_graph(x, y):
    plt.plot(x, y)
    plt.title('Antall solgte kolumbusbilletter fra 2015-06-01 til 2015-07-31')
    plt.xlabel("dato")
    plt.xticks(rotation=60)
    plt.ylabel("Billetter") # Antall bekreftet diagnoser
    plt.legend(loc='upper left')
    plt.grid(axis='y', linestyle='-')
    plt.grid(axis='x', linestyle='-')
    plt.show()

data = load_data()
x, y = totalt(data)
draw_line_graph(x, y)
x, y = daglig(data)
draw_line_graph(x, y)
x, y = periode(data)
draw_line_graph(x, y)

"""
alphab = ['A', 'B', 'C', 'D', 'E', 'F']
frequencies = [23, 44, 12, 11, 2, 10]

pos = np.arange(len(alphab))
width = 1.0     # gives histogram aspect to the bar diagram

ax = plt.axes()
ax.set_xticks(pos + (width / 2))
ax.set_xticklabels(alphab)

plt.bar(pos, frequencies, width, color='r')
plt.show()
"""
