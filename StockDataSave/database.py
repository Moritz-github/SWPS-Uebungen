# importing mysql-connector-python
import mysql.connector

with open("mysql-pwd.txt") as file:
    pwd = file.readlines()[0]


class DBManager:
    def __init__(self, symbol):
        self.symbol = symbol

        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd=pwd
        )
        self.cursor = self.db.cursor()

    def close(self):
        self.cursor.close()

    def init_table(self):
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS STOCKDATA")
        self.cursor.execute("USE STOCKDATA")
        # self.cursor.execute("DROP TABLE {}".format(self.symbol))
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS {} ( 
        date DATE PRIMARY KEY, 
        open DECIMAL(15,2), 
        high DECIMAL(15,2),
        low DECIMAL(15,2), 
        close DECIMAL(15,2), 
        volume int(13) )'''.format(self.symbol))

    def add_row_from_daily_price(self, DailyPrice):
        self.cursor.execute(
            'REPLACE INTO {} (date, open, high, low, close, volume) VALUES (DATE("{}"), {}, {}, {}, {}, {})'
            .format(self.symbol, DailyPrice.datestring, DailyPrice.open, DailyPrice.high,
                    DailyPrice.low, DailyPrice.close, DailyPrice.volume))
        self.db.commit()

    def print_all_values(self):
        self.cursor.execute("SELECT * FROM {}".format(self.symbol))

        for x in self.cursor:
            print(x)


if __name__ == "__main__":
    db = DBManager("TSLA")
    # db.add_value("2020-07-17", 385.3100)
    db.print_all_values()
