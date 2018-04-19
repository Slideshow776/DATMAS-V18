import sys, datetime, math
from openpyxl import load_workbook
import matplotlib.pyplot as plt
import numpy as np

sys.path.append('../Backend')
from Ruter import ruter
from NIPH import NIPH_ILS_graf, NIPH_virus_detections
from Kolumbus import kolumbus
from NPRA import NPRA_weekly, NPRA_monthly
from Twitter import twitter_analyzer

class double_y_graph:
    def __init__(self):
        # default season is 16/17
        self.NIPH_virus_Y = NIPH_virus_detections.NIPH_Virus().get_season_16_17() # [15_16, 16_17, 17_18]
        for _ in range(len(self.NIPH_virus_Y), 52): self.NIPH_virus_Y.append(None) # all graphs must have 52 units (weeks) on the x axis
        self.NIPH_ILI_Y = NIPH_ILS_graf.NIPH_ILI('../Backend/NIPH/ILI_tall_2016_17.xlsx').get_season_16_17() # [16_17]
        for _ in range(len(self.NIPH_ILI_Y), 52): self.NIPH_ILI_Y.append(None) # all graphs must have 52 units (weeks) on the x axis

    def get_NPRA_seasons_weekly(self, year_start, year_end, city='Norway'):
        filename = '../Backend/NPRA/Ukestrafikk 2013-2017 utvalgte punkter Bergen - Stavanger - Oslo.xlsx'
        workbook = load_workbook(filename)
        if city == 'Norway':
            cities, city_weeks1, city_weeks2 = ['Oslo', 'Bergen', 'Stavanger'], [], []
            y1, y2 = [0]*52, [0]*52
            for city in cities:
                worksheet = workbook[city]
                city_weeks1.append(NPRA_weekly.NPRA_weekly(filename).getData(year_start, worksheet, 40, 52))
                city_weeks2.append(NPRA_weekly.NPRA_weekly(filename).getData(year_end, worksheet, 0, 39))
            for city in city_weeks1:
                for i in range(len(city)):
                    y1[i] += city[i]
            for city in city_weeks2:
                for i in range(len(city)):
                    y2[i] += city[i]
        else:
            worksheet = workbook[city.lower().capitalize()]
            y1 = NPRA_weekly.NPRA_weekly(filename).getData(year_start, worksheet, 40, 52)
            y2 = NPRA_weekly.NPRA_weekly(filename).getData(year_end, worksheet, 0, 39)
        y = y1 + y2
        y = [x for x in y if x != 0]
        y.append(0)
        return y

    def set_season(self, season):
        if season == '15/16':
            self.NIPH_virus_Y = NIPH_virus_detections.NIPH_Virus().get_season_15_16() # [15_16, 16_17, 17_18]
            for _ in range(len(self.NIPH_virus_Y), 52): self.NIPH_virus_Y.append(None) # all graphs must have 52 units (weeks) on the x axis
        elif season == '16/17':
            self.NIPH_virus_Y = NIPH_virus_detections.NIPH_Virus().get_season_16_17() # [15_16, 16_17, 17_18]
            for _ in range(len(self.NIPH_virus_Y), 52): self.NIPH_virus_Y.append(None) # all graphs must have 52 units (weeks) on the x axis
        elif season == '17/18':
            self.NIPH_virus_Y = NIPH_virus_detections.NIPH_Virus().get_season_17_18() # [15_16, 16_17, 17_18]
            for _ in range(len(self.NIPH_virus_Y), 52): self.NIPH_virus_Y.append(None) # all graphs must have 52 units (weeks) on the x axis

    def get_twitter_seasons_weekly(self):
        filename = '../Backend/Twitter/twitter_data.txt'
        twitter_Y = twitter_analyzer.Twitter(filename).get_Y()
        twitter_X = twitter_analyzer.Twitter(filename).get_X()

        weeks = [None]*52
        offset = 12 # NIPH graph starts from week 40, so we need to offset by 12 so we start on week 0
        y, j, temp_week_number = [], 0, 0

        for i in range(len(twitter_X)):
            day = int(twitter_X[i][:twitter_X[i].find('.')])
            month = int(twitter_X[i][twitter_X[i].find('.')+1:twitter_X[i].find(' ')])
            year = int(twitter_X[i][twitter_X[i].find(' '):])

            week_number = datetime.date(year, month, day).isocalendar()[1]
            if i > 0:
                if temp_week_number == week_number: # += the y's
                    y[j] += twitter_Y[i]
                else: # make new entry                
                    j += 1
                    y.append(twitter_Y[i])
            else:
                y.append(twitter_Y[i])
            temp_week_number = week_number

        for i in range(len(y)):
            weeks[i + 7 + offset] = y[i] # 7 because our twitterdata starts on week 7      
        return weeks

    def get_kolumbus_seasons_weekly(self, year_start, year_end): # accepts season [15_16, 16_17]
        y_2015 = kolumbus.Kolumbus().get_Y_2015()
        y_2016 = kolumbus.Kolumbus().get_Y_2016()
        y_2017 = kolumbus.Kolumbus().get_Y_2017()

        JANUARY, OCTOBER, DECEMBER = 0, 8, 12 # October is the 9th month in the year (week number 40)
        season_months = []
        if year_start == 2015:
            for i in range(OCTOBER, DECEMBER): season_months.append(y_2015[i])
            for i in range(JANUARY, OCTOBER): season_months.append(y_2016[i])
        elif year_start == 2016:
            for i in range(OCTOBER, DECEMBER): season_months.append(y_2016[i])
            for i in range(JANUARY, OCTOBER): season_months.append(y_2017[i])
        
        weeks = [None]*52
        for i in range(len(weeks)):
            weeks[i] = season_months[math.floor(i/(52/12))] # 52 weeks divided by 12 months = 4.33 weeks per month ...
        return weeks

    def get_ruter_seasons_weekly(self, year_start, year_end): # accepts season [15_16, 16_17, 17_18]
        filename = '../Backend/Ruter/Antall påstigende per dag_Oslo_2015_2017.xlsx'
        y_2015 = ruter.Ruter(filename).get_y_2015()
        y_2016 = ruter.Ruter(filename).get_y_2016()
        y_2017 = ruter.Ruter(filename).get_y_2017()
        y_2018 = ruter.Ruter(filename).get_y_2018()
        for _ in range(len(y_2018), 365): y_2018.append(None)
        
        FIRST_DAY_IN_OCTOBER = math.ceil((365/12) * 9) # October is the 9th month in the year (week number 40)
        season_days = []
        if year_start == 2015:
            for i in range(FIRST_DAY_IN_OCTOBER, 365): season_days.append(y_2015[i])
            for i in range(0, FIRST_DAY_IN_OCTOBER): season_days.append(y_2016[i])
        elif year_start == 2016:
            for i in range(FIRST_DAY_IN_OCTOBER, 365): season_days.append(y_2016[i])
            for i in range(0, FIRST_DAY_IN_OCTOBER): season_days.append(y_2017[i])
        elif year_start == 2017:
            for i in range(FIRST_DAY_IN_OCTOBER, 365): season_days.append(y_2017[i])
            for i in range(0, FIRST_DAY_IN_OCTOBER): season_days.append(y_2018[i])
        
        weeks = [0]*52
        for i in range(len(season_days)-1): # -1 so we don't go out of bounds on the weeks
            if season_days[i]: 
                weeks[math.floor(math.floor(i/(365/52)))] += season_days[i]
        if season_days[364]: weeks[51] += season_days[364] # last day was skipped in loop, so we add it here
        weeks = [x for x in weeks if x != 0] # if we have any 0 values, delete them
        for _ in range(len(weeks), 52): weeks.append(None) # if we don't have 52 values, add Nones so we get 52 values
        return weeks

    def _double_y_graph(self, NIPH_type, y2, color1='#4286f4', color2='#872323'): # assumes common x-axis of 52 units (weeks)
        if NIPH_type.lower() == 'virus': y1 = self.NIPH_virus_Y
        elif NIPH_type.lower() == 'ili': y1 = self.NIPH_ILI_Y
        y1, y2 = np.array(y1), np.array(y2)

        x = []
        for i in range(52): x.append(i)
        x = np.array(x)

        fig, ax1 = plt.subplots()
        plt.figure(3)

        ax1.plot(x, y1, color=color1)
        ax1.set_ylabel('This is Y1', color=color1)
        ax1.tick_params('y', colors=color1)
        ax1.set_xticks(x)
        xticks_week40_til_week39 = ["40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39"]
        ax1.set_xticklabels(xticks_week40_til_week39)

        ax2 = ax1.twinx()
        ax2.plot(x, y2, color=color2)
        ax2.set_ylabel('This is Y2', color=color2)
        ax2.tick_params('y', colors=color2)

        fig.tight_layout()
        fig.patch.set_facecolor('#fff7ff')
        return fig

def main():    
    graphs = double_y_graph()
    graphs.set_season('15/16')
    graphs._double_y_graph( # twitter example
        'virus',
        graphs.get_kolumbus_seasons_weekly(2015, 2016)
    )
    plt.show()

if __name__ == '__main__':
    main()
