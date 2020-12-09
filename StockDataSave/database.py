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

        self.cursor.execute("CREATE DATABASE IF NOT EXISTS STOCKDATA")
        self.cursor.execute("USE STOCKDATA")
        # self.cursor.execute("DROP TABLE {}".format(self.symbol))
        self.cursor.execute("CREATE TABLE IF NOT EXISTS {} ( date DATE PRIMARY KEY, price DECIMAL(15,2) )".format(self.symbol))

    def add_value(self, datestring, price):
        self.cursor.execute("REPLACE INTO {} (date, price) VALUES (DATE(\"{}\"), {})".format(self.symbol, datestring, price))
        self.db.commit()

    def print_all_values(self):
        self.cursor.execute("SELECT * FROM {}".format(self.symbol))

        for x in self.cursor:
            print(x)


if __name__ == "__main__":
    db = DBManager("TSLA")
    # db.add_value("2020-07-17", 385.3100)
    db.print_all_values()
