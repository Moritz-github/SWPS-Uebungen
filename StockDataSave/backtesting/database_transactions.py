import mysql.connector
from datetime import datetime
from backtesting.transaction import Transaction

with open("../config/mysql-pwd.txt") as file:
    pwd = file.readlines()[0]

# klares Ziel:
# alle 3 Strategien für 1 Aktie, mit datenbank speicherung


class TransactionsDBManager:
    def __init__(self, symbol, table_name=""):
        self.symbol = symbol
        self.db = None
        self.cursor = None
        if table_name == "":
            self.table_name = "backtest " + datetime.now().strftime("%H:%M:%S %d-%m-%Y")
        else:
            self.table_name = table_name

        # print(f"Using table '{self.table_name}'")

        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd=pwd
        )

        self.cursor = self.db.cursor()

        self.cursor.execute("CREATE DATABASE IF NOT EXISTS BACKTESTINGSUITE")
        self.cursor.execute("USE BACKTESTINGSUITE")

        self.init_table()

    def init_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS `backtestingsuite`.`{}`  (
                              `date` DATE NOT NULL,
                              `symbol` VARCHAR(15) NOT NULL,
                              `buy_flag` BOOLEAN NOT NULL,
                              `count` INT NOT NULL,
                              `depotkonto` DECIMAL(14,3) NOT NULL,
                              `id` INT NOT NULL AUTO_INCREMENT,
                              PRIMARY KEY (`id`),
                              UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE);'''
                            .format(self.table_name))

    def close(self):
        self.cursor.close()

    def insert_transaction(self, transaction):
        x = transaction.date
        self.cursor.execute('INSERT INTO `{}` VALUES (DATE("{}"), "{}", {}, {}, {}, {});'
                            .format(self.table_name,
                                    transaction.date, transaction.symbol, transaction.buy_flag, transaction.count,
                                    transaction.depotkonto, transaction.id if transaction.id is not None else "Null"))
        self.db.commit()

    def get_alltime_latest_transaction(self):
        self.cursor.execute('SELECT * FROM `{}` ORDER BY ID DESC LIMIT 1;'.format(self.table_name))
        for x in self.cursor:
            return Transaction(x[0], x[1], x[2], x[3], x[4], x[5])
        return Transaction(-1, -1, -1, -1, -1, -1)

    def get_alltime_first_transaction(self):
        self.cursor.execute('SELECT * FROM `{}` ORDER BY ID ASC LIMIT 1;'.format(self.table_name))
        for x in self.cursor:
            return Transaction(x[0], x[1], x[2], x[3], x[4], x[5])
        return Transaction(-1, -1, -1, -1, -1, -1)

    def get_latest_transaction(self, date):
        self.cursor.execute('SELECT * FROM `{}` WHERE date < ("{}") ORDER BY ID DESC LIMIT 1;'
                            .format(self.table_name, date.strftime("%Y-%m-%d")))

        for x in self.cursor:
            return Transaction(x[0], x[1], x[2], x[3], x[4], x[5])
        return Transaction(-1, -1, -1, -1, -1, -1)

    def get_all_transactions(self):
        self.cursor.execute('SELECT * FROM `{}` ORDER BY ID ASC;'.format(self.table_name))
        transactions = []
        for x in self.cursor:
            transactions.append(Transaction(x[0], x[1], x[2], x[3], x[4], x[5]))
        return transactions


if __name__ == "__main__":
    db = TransactionsDBManager("IBM")

