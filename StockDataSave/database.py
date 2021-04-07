# importing mysql-connector-python
import mysql.connector
from datetime import datetime, timedelta
import DailyPrices

with open("mysql-pwd.txt") as file:
    pwd = file.readlines()[0]


class DBManager:
    def __init__(self, symbol):
        self.symbol = symbol
        self.db = None
        self.cursor = None

        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd=pwd
        )
        self.cursor = self.db.cursor()
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS STOCKDATA")
        self.cursor.execute("USE STOCKDATA")

    def close(self):
        self.cursor.close()

    def init_table(self):
        # Raw Data table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS {} ( 
                        date DATE PRIMARY KEY, 
                        open DECIMAL(15,2), 
                        high DECIMAL(15,2),
                        low DECIMAL(15,2), 
                        close DECIMAL(15,2),
                        volume int(13),
                        dividend DECIMAL(15,2),
                        split DECIMAL(15,2) )'''.format(self.symbol))

        # Calculated Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS {}_calc ( 
                                date DATE PRIMARY KEY, 
                                open DECIMAL(15,2), 
                                high DECIMAL(15,2),
                                low DECIMAL(15,2), 
                                close DECIMAL(15,2), 
                                volume int(13),
                                dividend DECIMAL(15,2),
                                split DECIMAL(15,2),
                                avg200 DECIMAL(15,2) )'''.format(self.symbol))

    def check_if_table_exists(self):
        try:
            self.cursor.execute("SELECT close from {}_calc limit 1;".format(self.symbol))
            for x in self.cursor:
                pass
            return True
        except:
            return False

    def insert_raw(self, DailyPrice):
        #   'REPLACE INTO'
        self.cursor.execute(
            'INSERT IGNORE INTO {} (date, open, high, low, close, volume, dividend, split) VALUES (DATE("{}"), {}, '
            '{}, {}, {}, {}, {}, {}) '.format(self.symbol, DailyPrice.datestring, DailyPrice.open, DailyPrice.high,
                                              DailyPrice.low, DailyPrice.close, DailyPrice.volume,
                                              DailyPrice.dividend, DailyPrice.split))
        self.db.commit()

    def insert(self, DailyPrice):
        #   'REPLACE INTO'
        self.cursor.execute(
            'REPLACE INTO {}_calc (date, open, high, low, close, volume, dividend, split, avg200) VALUES (DATE('
            '"{}"), {}, {}, {}, {}, {}, {}, {}, {}) '.format(self.symbol, DailyPrice.datestring, DailyPrice.open,
                                                             DailyPrice.high, DailyPrice.low, DailyPrice.close,
                                                             DailyPrice.volume, DailyPrice.dividend, DailyPrice.split,
                                                             DailyPrice.avg200))
        self.db.commit()

    def get_all_raw_values(self, desc=False):
        if not desc:
            self.cursor.execute("SELECT * FROM {};".format(self.symbol))
        else:
            self.cursor.execute("SELECT * FROM {} order by DATE Desc;".format(self.symbol))

        days = []
        for x in self.cursor:
            days.append(DailyPrices.DailyPrices(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7]))
        return days

    def get_values(self, start_date, end_date):
        self.cursor.execute('SELECT * FROM {}_calc where date > "{}" and date < "{}";'.
                            format(self.symbol, start_date, end_date))

        days = []
        for x in self.cursor:
            days.append(DailyPrices.DailyPrices(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8]))
        return days

    def get_day(self, date):
        self.cursor.execute('select * from {}_calc where date like ("{}")'.format(self.symbol, date))
        for x in self.cursor:
            print(x)
            return DailyPrices.DailyPrices(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8])
        return DailyPrices.DailyPrices(-1, -1, -1, -1, -1, -1, -1, -1, -1)

    def calc_200_average(self, date):
        # day = self.get_day(date)
        # if day is None:
        #    return None

        # else calculate 200 avg
        self.cursor.execute("with temp as (\
    select close from {}_calc where date <= '{}' order by date desc limit 200)\
    select avg(close) from temp;".format(self.symbol, date))

        for x in self.cursor:
            return x[0]
