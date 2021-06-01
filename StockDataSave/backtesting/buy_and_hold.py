import database
from backtesting.trading_strategy import TradingStrategy

class BuyAndHold(TradingStrategy):
    def __init__(self):
        super().__init__()

    def set_name(self):
        self.name = "Buy and Hold"

    def simulate_strategy(self):
        db = database.DBManager(self.symbol)
        start_dailyprice = db.get_closest_day(self.start_date)
        end_dailyprice = db.get_closest_day(self.end_date)

        self.roi = self.investment_amount * float(end_dailyprice.close / start_dailyprice.close)

if __name__ == "__main__":
    bnh = BuyAndHold()
