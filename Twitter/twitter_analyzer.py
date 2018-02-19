import time
import matplotlib.pyplot as plt
import numpy as np

"""
    time.struct gives: 
    time.struct_time(
        tm_year=2018,
        tm_mon=1,
        tm_mday=29,
        tm_hour=23,
        tm_min=59,
        tm_sec=35,
        tm_wday=0,
        tm_yday=29,
        tm_isdst=-1
        )
"""

def is_date(string):
    try:
        date = time.strptime(
            string,
            '%a %b %d %H:%M:%S %z %Y'
            )
        return date
    except ValueError:
        return False

def get_dates_from_file(file_name):
    FILE = open(file_name, "r+", encoding='utf-8')
    file_data = FILE.readlines()
    list_of_dates = []
    for data in file_data:
        temp = is_date(data.strip())
        if temp:
            list_of_dates.append(temp)
    return sorted(list_of_dates)

def make_the_graph(x, y, ticks):

    plt.xticks(x, ticks)
    plt.plot(np.array(x), np.array(y))

    plt.title('Tweets about influenza symptoms in Norway 2018')
    plt.xlabel("Date")
    plt.ylabel("Number of tweets")
    plt.grid(axis='y', linestyle='-')
    plt.grid(axis='x', linestyle='-')
    plt.show()

DATES = get_dates_from_file('twitter_data.txt')

D = {}
for date in DATES:
    date_format = str(date.tm_mday) + "." + str(date.tm_mon)+ " " + str(date.tm_year)
    if not date_format in D:
        D[date_format] = 1
    else:
        D[date_format] = D[date_format] + 1

X, Y, ticks = [], [], []
for keys in D:
    X.append(keys)
    Y.append(D[keys])

for i in range(0, len(D)):
    ticks.append(i)

make_the_graph(ticks, Y, X)