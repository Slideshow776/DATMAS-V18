# coding=utf8

import sys, csv
from openpyxl import load_workbook
import matplotlib.pyplot as plt, numpy as np

HOURLY_FILE_NAME = 'Stavanger/1100009 HILLEVÅGTUNNELEN 2013-2017.xlsx'
COORDINATES_STAVANGER_FILE_NAME = 'Stavanger/times nivå 1 STAVANGER.csv'
COORDINATES_BERGEN_FILE_NAME = 'Bergen/times nivå 1 BERGEN.csv'
COORDINATES_OSLO_FILE_NAME = 'Oslo/times nivå 1 OSLO.csv'
stavanger_stations, bergen_stations, oslo_stations = [], [], []

def print_all():
    liste = get_data_hourly('2013', HOURLY_FILE_NAME)

    #for d in get_data_hourly('2013', HOURLY_FILE_NAME):
        #print(d.get_all())
    print("\nYou ran the 'print_all' method, it prints all the data read from", HOURLY_FILE_NAME)

def wip():
    # d = {'dict1': {'foo': 1, 'bar': 2}, 'dict2': {'baz': 3, 'quux': 4}}
    """
    data = {
        '2013': {
            'field1': [], [], ...
            'field2': [], [], ...
            },
        ...
        }
    """
    data = {'2013': dict}
    years = ['2013']#, '2014'] #, '2015', '2016', '2017']
    for year in data.keys():
        for d in get_data_hourly(year):
            if d.get_field == 1: data[year]['field1'] = d.get_all
            elif d.get_field == 2: data[year]['field2'] = d.get_all
    
    print("HEYO!: ", data.get('2013'))

def combine_hourly_and_coordinates():
    data = get_data_hourly('2013', HOURLY_FILE_NAME)
    coordinates = get_coordinates(COORDINATES_STAVANGER_FILE_NAME)
    stations = get_data(data, coordinates)
    for s in stations:
        print(s.get_all())

def main():
    #combine_hourly_and_coordinates()
    print(
        get_all_coordinates(
            COORDINATES_STAVANGER_FILE_NAME,
            COORDINATES_BERGEN_FILE_NAME,
            COORDINATES_OSLO_FILE_NAME
        )
    )

def get_all_coordinates(stavanger, bergen, oslo):
    stavanger_coordinates = get_coordinates(stavanger)
    bergen_coordinates = get_coordinates(bergen)
    oslo_coordinates = get_coordinates(oslo)
    coordinates = []
    coordinates.append(stavanger_coordinates)
    coordinates.append(bergen_coordinates)
    coordinates.append(oslo_coordinates)

    pcoordinates = []
    for c in coordinates:
        for d in c:
            pcoordinates.append(d[1:])

    new_coords = []
    for p in pcoordinates:
        new_coords.append([float(p[0]), float(p[1])])

    return new_coords

def get_data(data, coordinates):
    for d in data:
        for c in coordinates:
            if c[0] == d.get_id():
                d.set_longitude(c[1])
                d.set_latitude(c[2])
                break
    return data

def get_data_hourly(year, filename): # returns data in a list of 'Traffic_recording_station' objects
    try:
        workbook = load_workbook(filename)
        worksheet = workbook[year]
        stations = []
        
        startid = int(HOURLY_FILE_NAME.find('/') + 1)
        endid = int(HOURLY_FILE_NAME.find(' '))
        id = HOURLY_FILE_NAME[startid:endid]        

        for i in range(4, worksheet.max_row):
            stations.append(
                    Traffic_recording_station(
                        id,
                        worksheet['A' + str(i)].value,
                        worksheet['B' + str(i)].value,
                        worksheet['C' + str(i)].value,
                        worksheet['D' + str(i)].value,
                        None,
                        None
                    )
            )
        print(stations[3].get_hour)
        return stations
    except: print('Error: Something went wrong loading the data from file or year')

def get_coordinates(filename):
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader, None)  # skip the headers
            coordinates = list(reader)
        return coordinates
    except:
        print('Error loading coordinates from ', filename)

class Traffic_recording_station:
    def __init__(self, id, date, hour, field, vehicles, longitude, latitude):
        self.id = id                #               Int
        self.date = date            # dd.mm.yyyy,   String
        self.hour = hour            # hh:mm,        String
        self.field = field          # 1 V 2,        Int
        self.vehicles = vehicles    # >= 0,         Int
        self.longitude = longitude  #               Float
        self.latitude = latitude    #               Float

    def set_id(self, id): self.id = id
    def set_date(self, date): self.date = date
    def set_hour(self, hour): self.hour = hour
    def set_field(self, field): self.field = field
    def set_vehicles(self, vehicles): self.vehicles = vehicles
    def set_longitude(self, longitude): self.longitude = longitude
    def set_latitude(self, latitude): self.latitude = latitude

    def get_id(self): return self.id
    def get_date(self): return self.date
    def get_hour(self): return self.hour
    def get_field(self): return self.field
    def get_vehicles(self): return self.vehicles
    def get_longitude(self): return self.longitude
    def get_latitude(self): return self.latitude
    def get_all(self):
        return (
            [
                self.id,
                self.date,
                self.hour,
                self.field,
                self.vehicles,
                self.longitude,
                self.latitude
            ]            
        )

if __name__ == '__main__':
    main()
