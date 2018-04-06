# coding=utf8

"""
    'Analyzes' the Twitter data collected by twitter_searching.py and draws a graph.
    The analyzation consists of simply counting how many tweets there are.

    @author Sandra Moen
"""

import time
import matplotlib.pyplot as plt
import numpy as np


class Twitter:
    def __init__(self, filepath):
        self.filepath = filepath
        DATES = self.get_dates_from_file(self.filepath)
        D = {}
        for date in DATES:
            date_format = str(date.tm_mday) + "." + str(date.tm_mon) + " " + str(date.tm_year)
            if not date_format in D: D[date_format] = 1
            else: D[date_format] = D[date_format] + 1

        X, Y, ticks = [], [], []
        for keys in D:
            X.append(keys)
            Y.append(D[keys])

        for i in range(len(D)):
            ticks.append(i)

        self._FIGURE = self.draw_graph(ticks, Y, X)

    def is_date(self, string):
        try: return time.strptime(string, '%a %b %d %H:%M:%S %z %Y')
        except ValueError: return False

    def get_dates_from_file(self, file_name):
            FILE = open(file_name, "r+", encoding='iso-8859-1')
            file_data = FILE.readlines()
            list_of_dates = []
            for data in file_data:
                temp = self.is_date(data.strip())
                if temp: list_of_dates.append(temp)
            return sorted(list_of_dates)

    def draw_graph(self, x, y, ticks):
        plt.figure(5)
        plt.xticks(x, ticks)
        plt.xticks(rotation=45)
        plt.plot(np.array(x), np.array(y))

        plt.title('Tweets about influenza symptoms in Norway 2018')
        plt.xlabel("Date")
        plt.ylabel("Number of tweets")
        plt.grid(axis='y', linestyle='-')
        plt.grid(axis='x', linestyle='-')
        figure = plt.figure(5)
        figure.patch.set_facecolor('#fff7ff')
        return figure

    def get_graph(self):
        return self._FIGURE

def main():
    Twitter('./twitter_data.txt').get_graph()
    plt.show()

if __name__ == '__main__':
    main()

