import matplotlib.pyplot as plt
import numpy as np
import datetime

class NIPH_ILI_oslo_bergen:
    def __init__(self, filepath_oslo, filepath_bergen, legend=True):
        oslo_data = self.get_data(filepath_oslo)
        bergen_data = self.get_data(filepath_bergen)

        self._FIGURE_OSLO = self.draw_graph(oslo_data, title=' in Oslo')
        self._FIGURE_BERGEN = self.draw_graph(bergen_data, title=' in Bergen', figure=1338)

        self._oslo_y_2014_2015 = oslo_data[0]
        self._oslo_y_2015_2016 = oslo_data[1]
        self._oslo_y_2016_2017 = oslo_data[2]
        self._oslo_y_2017_2018 = oslo_data[3]

        self._bergen_y_2014_2015 = bergen_data[0]
        self._bergen_y_2015_2016 = bergen_data[1]
        self._bergen_y_2016_2017 = bergen_data[2]
        self._bergen_y_2017_2018 = bergen_data[3]

    def _get_data_year(self, data, query_year):
        year = [None]*366
        for d in data:
            if query_year == d[0].year and d[0].isocalendar()[1] < 52:
                year[d[0].timetuple().tm_yday] = d
        return year

    def _get_first_part(self, data, query_year): # first part is week 40-52
        the_year = self._get_data_year(data, query_year)
        index = self._find_first_valid_day_of_week_40(the_year)

        part = []
        for i in range(len(the_year)):
            if i >= index:
                part.append(the_year[i])
        return part

    def _get_second_part(self, data, query_year): # second part is week 1-39
        the_year = self._get_data_year(data, query_year)
        index = self._find_first_valid_day_of_week_40(the_year)

        part = []
        for i in range(len(the_year)):
            if i < index:
                part.append(the_year[i])
        return part

    def _find_first_valid_day_of_week_40(self, year):
        index = 0
        for i in range(len(year)):
            try: 
                if year[i][0].isocalendar()[1] == 40:
                    index = i
            except:
                pass
        return index

    def get_data(self, filepath): # retruns ILI seasons, week40-week40
        with open(filepath) as f: 
            lines = f.readlines()
        f.close() # remember to close resources after use

        data = []
        for line in lines[1:]:
            entry = line.split()
            date = datetime.datetime(int(entry[0][6:]), int(entry[0][3:5]), int(entry[0][:2]))
            _sum = 0
            for e in entry: # aggregate incidents and ignore 'NA's
                try: _sum += int(e)
                except: pass
            data.append([date, _sum])

        season_14_15 = self._get_second_part(data, 2015)
        season_15_16 = self._get_first_part(data, 2015) + self._get_second_part(data, 2016)
        season_16_17 = self._get_first_part(data, 2016) + self._get_second_part(data, 2017)
        season_17_18 = self._get_first_part(data, 2017) + self._get_second_part(data, 2018)

        for i in range(len(season_14_15)):
            try: print(season_14_15[i][1])
            except: pass

        return [season_14_15, season_15_16, season_16_17, season_17_18]

    def draw_graph(self, data, legend=True, title='', figure=1337):
        plt.figure(figure)
        x, ticks = [], [] # in order to get the correct x axis...
        for i in range(92, 366): ticks.append(i) # week 40 starts on about day 274
        for i in range(1, 92): ticks.append(i)
        print(ticks)
        for i in range(365): x.append(i)
        plt.xticks(ticks, x)
        plt.xticks(rotation=45)

        label = ["2014/2015", "2015/2016", "2016/2017", "2017/2018"]
        if not legend: # choose not to have duplicate labels with legend = False
            for i in range(len(label)): label[i] = '_' + label[i]
        
        temp = []
        for j in range(len(data)):
            for i in range(365):
                try: temp.append(data[j][i][1]) 
                except: temp.append(None) # TODO: this is just wrong ...
            plt.plot(x, temp, label=label[j])
            temp = []
        
        plt.title('Influenza seasons' + title)
        plt.xlabel("Day of year")
        plt.ylabel("ILI")
        if legend: plt.legend(loc='upper left')

        plt.grid(axis='y', linestyle='-')
        plt.grid(axis='x', linestyle='-')
        figure = plt.figure(figure)
        figure.patch.set_facecolor('#fff7ff')
        return figure
    
    def get_graph_oslo(self): return self._FIGURE_OSLO
    def get_graph_bergen(self): return self._FIGURE_BERGEN

    def get_oslo_season_14_15(self): return self._oslo_y_2014_2015
    def get_oslo_season_15_16(self): return self._oslo_y_2015_2016
    def get_oslo_season_16_17(self): return self._oslo_y_2016_2017
    def get_oslo_season_17_18(self): return self._oslo_y_2017_2018 
       
    def get_bergen_season_14_15(self): return self._bergen_y_2014_2015
    def get_bergen_season_15_16(self): return self._bergen_y_2015_2016
    def get_bergen_season_16_17(self): return self._bergen_y_2016_2017
    def get_bergen_season_17_18(self): return self._bergen_y_2017_2018

def main():
    NIPH_ILI_oslo_bergen(
        r'C:\Users\Slideshow\Dropbox\School\DATMAS-V18\fra Lars\Sykdomspuls\InfluensaOsloPerDag20180430_2015_2018.txt',
        r'C:\Users\Slideshow\Dropbox\School\DATMAS-V18\fra Lars\Sykdomspuls\InfluensaBergenPerDag_20180430_2015_2018.txt'
    ) # absolute path to protect sensitive data
    plt.show()

if __name__ == '__main__':
    main()
