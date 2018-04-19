"""
    Shows a graph of influenza seasons 2015/2016, 2016/2017 and 2017/2018
    Data is hardcoded because it is only available in pdf files.

    @ Sandra Moen
"""

import matplotlib.pyplot as plt
import numpy as np

class NIPH_Virus:
    def __init__(self):
        self.y_2015_2016 = np.array([1126*.04, 1465*.002, 1551*.002, 1776*.003, 1641*.009, 1853*.015, 1921*.022, 2050*.029, 2046*.036, 2241*.043, 2467*.052, 2703*.072, 2227*.109, 2033*.116, 3622*.099, 3478*.105, 3235*.166, 4373*.209, 4858*.235, 5192*.245, 5589*.235, 4957*.272, 4877*.256, 4432*.227, 4027*.242, 2376*.213, 3096*.173, 3189*.145, 2837*.13, 2506*.106, 2573*.088, 2208*.08, 2036*.08, 1745*.042, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None])
        self.y_2016_2017 = np.array([2274*.004, 2419*.004, 2686*.006, 2706*.014, 3000*.024, 3080*.03, 3500*.055, 3725*.082, 4206*.112, 5231*.184, 3248*.229, 6772*.272, 5286*.278, 8017*.222, 7420*.172, 6402*.165, 6038*.163, 6059*.147, 5648*.136, 4912*.143, 5102*.152, 4494*.134, 4237*.115, 4024*.115, 3800*.109, 3753*.106, 3477*.101, 2017*.098, 2865*.082, 3090*.072, 2450*.077, 2888*.104, 2807*.103, 3039*.092, 3103*.055, 2052*.04, 2034*.025, 1526*.029, 1143*.017, 1097*.021, 1168*.014, 794*.014, 514*.016, 557*.014, 591*.017, 644*.014, 994*.011, 201*.03, 585*.015, 317*.016, 281*.004, 497*.004])
        self.y_2017_2018 = np.array([2349*.006, 3007*.006, 3219*.007, 3782*.009, 4140*.013, 4387*.014, 4472*.025, 4539*.022, 4671*.037, 5235*.054, 5722*.084, 6367*.149, 4438*.223, 7933*.216, 8417*.209, 7894*.252, 8475*.291, 8998*.291, 8878*.337, 9093*.36, 7677*.298, 7417*.285, 7073*.264, 6562*.248, 3601*.214, 4648*.172, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None])
        self._FIGURE = self._draw_graph()

    def _draw_graph(self):
        plt.figure(3)        
        x_weeks_of_year = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29 ,30 ,31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51])
        xticks_week40_til_week39 = ["40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39"]
        
        plt.xticks(x_weeks_of_year, xticks_week40_til_week39)
        plt.plot(x_weeks_of_year, self.y_2015_2016, label="2015/2016")
        plt.plot(x_weeks_of_year, self.y_2016_2017, label="2016/2017")
        plt.plot(x_weeks_of_year, self.y_2017_2018, label="2017/2018")

        plt.title('Influenza seasons in Norway')
        plt.xlabel("Week")
        plt.ylabel("Virus observations")
        plt.legend(loc='upper left')
        plt.grid(axis='y', linestyle='-')
        plt.grid(axis='x', linestyle='-')
        figure = plt.figure(3)
        figure.patch.set_facecolor('#fff7ff')
        return figure
    
    def get_season_15_16(self): return self.y_2015_2016
    def get_season_16_17(self): return self.y_2016_2017
    def get_season_17_18(self): return self.y_2017_2018
    def get_graph(self): return self._FIGURE

def main():
    NIPH_Virus().get_graph()
    plt.show()

if __name__ == '__main__':
    main()
