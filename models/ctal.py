import datetime

from flask import jsonify
from pandas import read_csv


class CTAL:
    df_ctalrides = None
    ctalrides = []

    def __init__(self):
        # initialize and get ridership data
        print('initializing CTA L data')
        # self.df_ctalrides = read_csv('../raw_data/CTA_-_Ridership_-__L__Station_Entries_-_Daily_Totals_20240721.csv')
        self.df_ctalrides = read_csv('raw_data/CTA_-_Ridership_-__L__Station_Entries_-_Daily_Totals_20240721.csv')

        self.df_ctalrides.reset_index()  # make sure indexes pair with number of rows

        for index, row in self.df_ctalrides.iterrows():
            ctalride = CTALride()
            ctalride.station_id = row['station_id']
            ctalride.station_name = row['stationname']
            ctalride.date = row['date']
            ctalride.day_type = row['daytype']
            ctalride.rides = row['rides']
            self.ctalrides.append(ctalride)

    def getdata(self):
        returnctalrides = []
        for ride in self.ctalrides:
            returnctalrides.append(ride.serialize())
        return returnctalrides

    def printdata(self):
        print('printing CTA L data')
        # print(self.df_ctalrides)
        # print(self.df_ctalrides['station_id'])
        # print(self.df_ctalrides['stationname'])
        # print(self.df_ctalrides['date'])
        # print(self.df_ctalrides['daytype'])
        # print(self.df_ctalrides['rides'])
        for ride in self.ctalrides:
            print(ride)


class CTALride:
    station_id = str
    station_name = str
    date = datetime
    day_type = str
    rides = int

    def __str__(self):
        return ('Ride: ' + str(self.station_id) + ', '
                + str(self.station_name) + ', '
                + str(self.date) + ', '
                + str(self.day_type) + ', '
                + str(self.rides) + ', ')

    def serialize(self):
        return ({'station_id': int(self.station_id),
                'station_name': str(self.station_name),
                'date': str(self.date),
                'day_type': str(self.day_type),
                'rides': int(self.rides)})
