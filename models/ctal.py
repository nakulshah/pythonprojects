from pandas import read_csv


class CTAL:
    df_ctalrides = None

    def __init__(self):
        # initialize and get ridership data
        print('initializing CTA L data')
        self.df_ctalrides = read_csv('raw_data/CTA_-_Ridership_-__L__Station_Entries_-_Daily_Totals_20240721.csv')

    def getdata(self):
        return self.df_ctalrides

    def printdata(self):
        print('printing CTA L data')
        print(self.df_ctalrides)