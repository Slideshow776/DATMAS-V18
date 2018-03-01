"""
    'Analyzes' the Twitter data collected by twitter_searching.py.
    The analyzation consists of simply counting how many tweets there are.

    @author Sandra Moen
"""

import time
import matplotlib.pyplot as plt
import numpy as np

def is_date(string):
    try: return time.strptime(string, '%a %b %d %H:%M:%S %z %Y')
    except ValueError: return False

def get_dates_from_file(file_name):
    FILE = open(file_name, "r+", encoding='iso-8859-1')
    file_data = FILE.readlines()
    list_of_dates = []
    for data in file_data:
        temp = is_date(data.strip())
        if temp: list_of_dates.append(temp)
    return sorted(list_of_dates)

def draw_graph(x, y, ticks):
    plt.xticks(x, ticks)
    plt.plot(np.array(x), np.array(y))

    plt.title('Tweets about influenza symptoms in Norway 2018')
    plt.xlabel("Date")
    plt.ylabel("Number of tweets")
    plt.grid(axis='y', linestyle='-')
    plt.grid(axis='x', linestyle='-')
    plt.show()

def main():
    DATES = get_dates_from_file('twitter_data.txt')
    D = {}
    for date in DATES:
        date_format = str(date.tm_mday) + "." + str(date.tm_mon)+ " " + str(date.tm_year)
        if not date_format in D: D[date_format] = 1
        else: D[date_format] = D[date_format] + 1

    X, Y, ticks = [], [], []
    for keys in D:
        X.append(keys)
        Y.append(D[keys])

    for i in range(len(D)):
        ticks.append(i)

    draw_graph(ticks, Y, X)

main()
