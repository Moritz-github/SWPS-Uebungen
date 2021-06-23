from abc import ABC, abstractmethod
import datetime
from database import DBManager
from backtesting.database_transactions import TransactionsDBManager

class DataNotInDataset(Exception):
    def __init__(self, message="The data is not available in the dataset"):
        self.message = message
        super().__init__(message)

class TradingStrategy(ABC):
    def __init__(self, symbol=None, start_date=None, end_date=None, amount=None):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.investment_amount = amount

        # überprüfen, ob daten am start_datum schon vorhanden waren
        db = DBManager(self.symbol)
        if db.get_closest_day(start_date).close == -1:
            raise DataNotInDataset

        self.set_name()

        # self.check_data_exists()

        self.ask_input()

        self.trans_db = TransactionsDBManager(self.symbol)

        self.simulate_strategy()
        self.print_roi()

    def check_data_exists(self):
        pass # toDO

    @abstractmethod
    def set_name(self):
        pass

    @abstractmethod
    def simulate_strategy(self):
        pass

    def ask_input(self):
        while self.symbol is None or self.symbol == "":
            self.symbol = input(
                "Bei welcher Aktie wollen Sie ein Investment Simulieren? (z.B. Apple ... AAPL; Tesla ... TSLA; Amazon "
                "... AMZN)\n")

        while not isinstance(self.start_date, datetime.date):
            invest_date_input = input('Investment-Datum ("2010-01-01") -> enter): ')
            if invest_date_input == "":
                invest_date_input = "2010-01-01"
            self.start_date = datetime.datetime.strptime(invest_date_input, "%Y-%m-%d").date()

        while not isinstance(self.end_date, datetime.date):
            end_date_input = input('Auszahl-Datum (falls bis heute -> enter): ')
            if end_date_input != "":
                self.end_date = datetime.datetime.strptime(end_date_input, "%Y-%m-%d").date()
            else:
                self.end_date = datetime.datetime.now().date()

        while self.investment_amount is None or self.investment_amount <= 0:
            investment_amount_input = input("Wie viel Geld soll Investiert werden? (100k -> enter): ")
            if investment_amount_input == "":
                investment_amount_input = 100_000
            self.investment_amount = float(investment_amount_input)


    def print_roi(self):
        print(f"Ein investment in {self.symbol} von {self.investment_amount:.0f}€ am {self.start_date} mit der " \
                f"Handelsstrategie '{self.name}' bis zum {self.end_date} wären nun {self.roi:.2f}. " \
                  f"({self.roi/self.investment_amount*100-100:.2f}%)")

