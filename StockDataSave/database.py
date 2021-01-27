# importing mysql-connector-python
import mysql.connector
from datetime import datetime, timedelta

with open("mysql-pwd.txt") as file:
    pwd = file.readlines()[0]


class DBManager:
    def __init__(self, symbol):
        self.symbol = symbol
        self.db = None
        self.cursor = None

    def close(self):
        self.cursor.close()

    def init_table(self):
        # self.cursor.execute("DROP TABLE {}".format(self.symbol))
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS {} ( 
                date DATE PRIMARY KEY, 
                open DECIMAL(15,2), 
                high DECIMAL(15,2),
                low DECIMAL(15,2), 
                close DECIMAL(15,2), 
                volume int(13) )'''.format(self.symbol))

    def open(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd=pwd
        )
        self.cursor = self.db.cursor()
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS STOCKDATA")
        self.cursor.execute("USE STOCKDATA")

    def check_if_table_exists(self):
        try:
            self.cursor.execute("SELECT close from {} limit 1;".format(self.symbol))
            for x in self.cursor:
                pass
            return True
        except:
            return False

    def add_row_from_daily_price(self, DailyPrice):
        #   'REPLACE INTO'
        self.cursor.execute(
            'INSERT IGNORE INTO {} (date, open, high, low, close, volume) VALUES (DATE("{}"), {}, {}, {}, {}, {})'
                .format(self.symbol, DailyPrice.datestring, DailyPrice.open, DailyPrice.high,
                        DailyPrice.low, DailyPrice.close, DailyPrice.volume))
        self.db.commit()

    def print_all_values(self):
        self.cursor.execute("SELECT * FROM {}".format(self.symbol))

        for x in self.cursor:
            print(x)

    def get_last_x_days(self, x):
        self.cursor.execute(
            'SELECT close FROM {} ORDER BY DATE desc LIMIT {};'.format(self.symbol, x))

        return [x[0] for x in self.cursor]

    def get_day(self, date):
        self.cursor.execute('select close from {} where date = DATE("{}")'.format(self.symbol, date))
        for x in self.cursor:
            return x[0]

    def get_200_average(self, date):
        # self.cursor.execute('SELECT avg(items.close) from \
        #                        (SELECT close FROM {} t WHERE t.date < DATE("{}") \
        #                        ORDER BY t.date desc limit 200) items;'.format(self.symbol, date))
        # for x in self.cursor:
        #    return x[0]
        day = self.get_day(date)
        if day is None:
            return None

        self.cursor.execute("with temp as (\
    select close from {} where date <= '{}' order by date desc limit 200)\
    select avg(close) from temp;".format(self.symbol, date))

        for x in self.cursor:
            return x[0]

        # self.cursor.execute('select close from {} where date < DATE("{}") order by date desc limit 200;'.format(self.symbol, date))
        # y = [x[0] for x in self.cursor]
        # print(y)
        # return sum(y) / len(y)


if __name__ == "__main__":
    db = DBManager("tslaa")
    db.open()
    # db.add_value("2020-07-17", 385.3100)
    print(db.check_if_table_exists())
    db.close()
