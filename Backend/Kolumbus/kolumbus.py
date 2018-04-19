"""
    Shows a graph of total number of tickets sold by Kolumbus in the years 2015-2017 by monthly basis.
    Data is hardcoded because it was provided to me by a .PNG file (yes I know ...)

    @author Sandra Moen
"""

import matplotlib.pyplot as plt
import numpy as np

class Kolumbus:
    def __init__(self):
        self._FIGURE = self._draw_graph()

    def _draw_graph(self):
        plt.figure(4)
        ticks = ['January', 'February', 'March', 'April',
                'May', 'June', 'July', 'August',
                'Spetember', 'October', 'November', 'December']

        # 2015
        x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
        self.Y_2015 = np.array([1572228, 1426184, 1603735, 1417790, 1394289, 1381852, 895238, 1407594, 1712808, 1642499, 1634379, 1372222])
        self.Y_2016 = np.array([1672432, 1537624, 1435002, 1586622, 1463891, 1398755, 900158, 1442876, 1686364, 1609436, 1706720, 1384717])
        self.Y_2017 = np.array([1804157, 1587487, 1786241, 1443892, 1670943, 1445117, 998763, 1633687, 1807639, 1690222, 1762062, 1338353])

        plt.xticks(x, ticks)
        plt.plot(x, self.Y_2015, label="2015")
        plt.plot(x, self.Y_2016, label="2016")
        plt.plot(x, self.Y_2017, label="2017")

        plt.title('Total number of sold Kolumbus tickets')
        plt.xlabel("Months")
        plt.ylabel("Tickets")
        plt.legend(loc='upper left')
        plt.grid(axis='y', linestyle='-')
        plt.grid(axis='x', linestyle='-')
        figure = plt.figure(4)
        figure.patch.set_facecolor('#fff7ff')
        return figure

    def get_graph(self): return self._FIGURE
    def get_Y_2015(self): return self.Y_2015
    def get_Y_2016(self): return self.Y_2016
    def get_Y_2017(self): return self.Y_2017

def main():
    Kolumbus().get_graph()
    plt.show()

if __name__ == '__main__':
    main()
