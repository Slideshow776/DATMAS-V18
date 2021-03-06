import matplotlib.pyplot as plt
import numpy as np
import datetime

"""
@author: Sandra Moen
"""
class NIPH_ILI_oslo_bergen:
    def __init__(self, filepath_oslo, filepath_bergen, legend=True):
        oslo_data = self._get_data(filepath_oslo)
        bergen_data = self._get_data(filepath_bergen)
        
        self._FIGURE_OSLO_DAILY = self.draw_graph_daily(oslo_data, legend, title=' in Oslo')
        self._FIGURE_BERGEN_DAILY = self.draw_graph_daily(bergen_data, legend, title=' in Bergen', figure=1338)

        self._oslo_y_2014_2015 = oslo_data[0]
        self._oslo_y_2015_2016 = oslo_data[1]
        self._oslo_y_2016_2017 = oslo_data[2]
        self._oslo_y_2017_2018 = oslo_data[3]

        self._bergen_y_2014_2015 = bergen_data[0]
        self._bergen_y_2015_2016 = bergen_data[1]
        self._bergen_y_2016_2017 = bergen_data[2]
        self._bergen_y_2017_2018 = bergen_data[3]

        self.oslo_data_weekly = self._aggregate_data_from_daily_to_weekly(oslo_data)
        self._FIGURE_OSLO_WEEKLY = self.draw_graph_weekly(self.oslo_data_weekly, legend, title=' in Oslo', figure=1339)

        self.bergen_data_weekly = self._aggregate_data_from_daily_to_weekly(bergen_data)
        self._FIGURE_BERGEN_WEEKLY = self.draw_graph_weekly(self.bergen_data_weekly, legend, title=' in Bergen', figure=1340)

    def _aggregate_data_from_daily_to_weekly(self, data):
        weekly_seasons = []
        weekly_data = []*52
        counter = 0
        _sum = 0
        for season in data:
            for d in season:
                counter += 1
                try: _sum += d
                except: pass

                if counter is 7:
                    if _sum is 0: _sum = None
                    weekly_data.append(_sum)
                    counter = _sum = 0
            weekly_seasons.append(weekly_data)
            weekly_data = []*52
            counter = _sum = 0
        return weekly_seasons

    def _get_data(self, filepath): # retruns ILI seasons, week40-week40
        with open(filepath) as f: 
            lines = f.readlines()
        f.close() # remember to close resources after use

        data = []
        for line in lines[1:]: # skip the header
            entry = line.split()
            date = datetime.datetime(int(entry[0][6:]), int(entry[0][3:5]), int(entry[0][:2]))
            _sum = 0
            for e in entry: # aggregate incidents and ignore 'NA's
                try: _sum += int(e)
                except: pass
            data.append([date, _sum])

        year_2015, year_2016, year_2017, year_2018 = [None]*366, [None]*366, [None]*366, [None]*366
        for d in data:
            if 2015 == d[0].year and d[0].isocalendar()[1] < 52:
                year_2015[d[0].timetuple().tm_yday] = d[1]
            elif 2016 == d[0].year and d[0].isocalendar()[1] < 52:
                year_2016[d[0].timetuple().tm_yday] = d[1]
            elif 2017 == d[0].year and d[0].isocalendar()[1] < 52:
                year_2017[d[0].timetuple().tm_yday] = d[1]
            elif 2018 == d[0].year and d[0].isocalendar()[1] < 52:
                year_2018[d[0].timetuple().tm_yday] = d[1]

        season_14_15, season_15_16, season_16_17, season_17_18 = [None]*366, [None]*366, [None]*366, [None]*366
        season_14_15 = [None]*(366-273) + year_2015[:273]
        season_15_16 = year_2015[273:] + year_2016[:273]
        season_16_17 = year_2016[273:] + year_2017[:273]
        season_17_18 = year_2017[273:] + year_2018[:273]

        return [season_14_15, season_15_16, season_16_17, season_17_18]

    def draw_graph_weekly(self, data, legend=True, title='', figure=4444):
        plt.figure(figure)
        x, ticks = [], [] # in order to get the correct x axis...
        for i in range(40, 53): ticks.append(i) # week 40 starts on about day 274
        for i in range(1, 40): ticks.append(i)
        for i in range(52): x.append(i)

        plt.xticks(x, ticks)
        plt.xticks(rotation=45)

        label = ["2014/2015", "2015/2016", "2016/2017", "2017/2018"]
        if not legend: # choose not to have duplicate labels with legend = False
            for i in range(len(label)): label[i] = '_' + label[i]
                    
        for j in range(len(data)):
            plt.plot(x, data[j], label=label[j])
        
        plt.title('Influenza seasons' + title)
        plt.xlabel("Week of year")
        plt.ylabel("ILI")
        if legend: plt.legend(loc='upper left')

        plt.grid(axis='y', linestyle='-')
        plt.grid(axis='x', linestyle='-')
        figure = plt.figure(figure)
        figure.patch.set_facecolor('#fff7ff')
        return figure

    def draw_graph_daily(self, data, legend=True, title='', figure=1337):
        plt.figure(figure)
        x, ticks = [], [] # in order to get the correct x axis...
        for i in range(92, 366): ticks.append(i) # week 40 starts on about day 274
        for i in range(1, 92): ticks.append(i)
        for i in range(366): x.append(i)
        plt.xticks(ticks, x)
        plt.xticks(rotation=45)

        label = ["2014/2015", "2015/2016", "2016/2017", "2017/2018"]
        if not legend: # choose not to have duplicate labels with legend = False
            for i in range(len(label)): label[i] = '_' + label[i]
                    
        for j in range(len(data)):
            plt.plot(x, data[j], label=label[j])
        
        plt.title('Influenza seasons' + title)
        plt.xlabel("Day of year")
        plt.ylabel("ILI")
        if legend: plt.legend(loc='upper left')

        plt.grid(axis='y', linestyle='-')
        plt.grid(axis='x', linestyle='-')
        figure = plt.figure(figure)
        figure.patch.set_facecolor('#fff7ff')
        return figure
    
    def get_graph_oslo_daily(self): return self._FIGURE_OSLO_DAILY
    def get_graph_bergen_daily(self): return self._FIGURE_BERGEN_DAILY

    def get_graph_oslo_weekly(self): return self._FIGURE_OSLO_WEEKLY
    def get_graph_bergen_weekly(self): return self._FIGURE_BERGEN_WEEKLY

    def get_oslo_season_14_15(self): return self._oslo_y_2014_2015
    def get_oslo_season_15_16(self): return self._oslo_y_2015_2016
    def get_oslo_season_16_17(self): return self._oslo_y_2016_2017
    def get_oslo_season_17_18(self): return self._oslo_y_2017_2018 

    def get_bergen_season_14_15(self): return self._bergen_y_2014_2015
    def get_bergen_season_15_16(self): return self._bergen_y_2015_2016
    def get_bergen_season_16_17(self): return self._bergen_y_2016_2017
    def get_bergen_season_17_18(self): return self._bergen_y_2017_2018

    def get_oslo_seasons_weekly(self): return self.oslo_data_weekly
    def get_bergen_seasons_weekly(self): return self.bergen_data_weekly

def main():
    NIPH_ILI_oslo_bergen(
        r'C:\Users\Slideshow\Dropbox\School\DATMAS-V18\fra Lars\Sykdomspuls\InfluensaOsloPerDag20180430_2015_2018.txt',
        r'C:\Users\Slideshow\Dropbox\School\DATMAS-V18\fra Lars\Sykdomspuls\InfluensaBergenPerDag_20180430_2015_2018.txt'
    ) # absolute path to protect sensitive data
    plt.show()

if __name__ == '__main__':
    main()
