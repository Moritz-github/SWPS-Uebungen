import database
from backtesting.trading_strategy import TradingStrategy
from backtesting.transaction import Transaction
import datetime
import decimal

class BuyAndHold(TradingStrategy):
    def __init__(self, symbol=None, start_date=None, end_date=None, amount=None):
        super().__init__(symbol=symbol, start_date=start_date, end_date=end_date, amount=amount)

    def set_name(self):
        self.name = "Buy and Hold"

    def simulate_strategy(self):
        self.db = database.DBManager(self.symbol)

        count = int(decimal.Decimal(self.investment_amount) / decimal.Decimal(self.db.get_closest_raw_day(self.start_date).close))
        self.trans_db.insert_transaction(Transaction(self.start_date, self.symbol, 1, count, 0))

        # alle tage holen und in self.days_dict speichern
        days = self.db.get_all_values()
        days_dict = {}
        for day in days:
            days_dict[day.datestring] = day

        # split correction
        running_date = self.start_date
        while running_date < self.end_date:
            if running_date in days_dict.keys() and days_dict[running_date].split != 1:
                count *= days_dict[running_date].split
            self.trans_db.insert_transaction(Transaction(running_date, self.symbol, 1, count, 0))
            running_date += datetime.timedelta(days=1)

        self.trans_db.insert_transaction(Transaction(self.end_date, self.symbol, 0, 0,
                                                     decimal.Decimal(count)*decimal.Decimal(self.db.get_raw_day(self.end_date).close)))

        self.roi = float(count)*float(self.db.get_closest_raw_day(self.end_date).close)


if __name__ == "__main__":
    bnh = BuyAndHold()
