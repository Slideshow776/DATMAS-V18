import matplotlib.pyplot as plt
import numpy as np

ticks = ['January', 'February', 'March', 'April',
            'May', 'June', 'July', 'August', 'Spetember',
            'October', 'November', 'December']

# 2015
x_2015 = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
y_2015 = np.array([1572228, 1426184, 1603735, 1417790, 1394289, 1381852, 895238, 1407594, 1712808, 1642499, 1634379, 1372222])

# 2016
x_2016 = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
y_2016 = np.array([1672432, 1537624, 1435002, 1586622, 1463891, 1398755, 900158, 1442876, 1686364, 1609436, 1706720, 1384717])

# 2017
x_2017 = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
y_2017 = np.array([1804157, 1587487, 1786241, 1443892, 1670943, 1445117, 998763, 1633687, 1807639, 1690222, 1762062, 1338353])

plt.xticks(x_2015, ticks)
plt.plot(x_2015, y_2015, label="2015")
plt.plot(x_2016, y_2016, label="2016")
plt.plot(x_2017, y_2017, label="2017")

plt.title('Total number of sold Kolumbus tickets')
plt.xlabel("Months")
plt.ylabel("Tickets")
plt.legend(loc='upper left')
plt.grid(axis='y', linestyle='-')
plt.grid(axis='x', linestyle='-')
plt.show()