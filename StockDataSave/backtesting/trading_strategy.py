from abc import ABC, abstractmethod
import datetime

class TradingStrategy(ABC):
    def __init__(self):
        self.set_name()

        # self.check_data_exists()

        self.ask_input()
        self.simulate_strategy()
        self.print_roi()

    def check_data_exists():
        pass # toDO

    @abstractmethod
    def set_name(self):
        pass

    @abstractmethod
    def simulate_strategy(self):
        pass

    def ask_input(self):
        self.symbol = input(
            "Bei welcher Aktie wollen Sie ein Investment Simulieren? (z.B. Apple ... AAPL; Tesla ... TSLA; Amazon "
            "... AMZN)\n")
        self.start_date = datetime.datetime.strptime(input('Investment-Datum (z.B. "2010-01-01"): '), "%Y-%m-%d").date()

        end_date_input = input('Auszahl-Datum (falls bis heute -> enter): ')
        if end_date_input != "":
            self.end_date = datetime.datetime.strptime(end_date_input, "%Y-%m-%d")
        else:
            self.end_date = datetime.datetime.now().date()

        self.investment_amount = float(input("Wie viel Geld soll Investiert werden?"))

    def print_roi(self):
        print(f"Ein investment in {self.symbol} von {self.investment_amount:.0f}€ am {self.start_date} mit der " \
                f"Handelsstrategie '{self.name}' bis zum {self.end_date} wären nun {self.roi:.2f}. " \
                  f"({self.roi/self.investment_amount*100:.2f}%)")

