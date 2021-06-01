import datetime


class Transaction:
    def __init__(self, date, symbol, buy_flag, count, depotkonto, id=None):
        self.id = id
        self.date = date
        self.symbol = symbol
        self.buy_flag = buy_flag
        self.count = count
        self.depotkonto = depotkonto

    def __str__(self):
        return f"{self.id}, {self.date}, {self.symbol}, {self.buy_flag}, {self.count}, {self.depotkonto}"