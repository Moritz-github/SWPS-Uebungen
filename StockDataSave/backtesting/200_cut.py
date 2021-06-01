import datetime
import decimal
import database
from backtesting import database_transactions
from backtesting.transaction import Transaction
from backtesting.display_200_strat import display_200
from backtesting.trading_strategy import TradingStrategy

# https://pyinvesting.com/backtest/moving-average/moving-average-preview/amzn/Simple/200

class AVG200Strat(TradingStrategy):
    def __init__(self):
        super().__init__()

    def set_name(self):
        self.name = "200-er Schnitt"

    def simulate_strategy(self):
        trans_db = database_transactions.TransactionsDBManager(self.symbol)
        db = database.DBManager(self.symbol)

        dummy_transaction = Transaction(self.start_date, "DUMMY", False, 0, self.investment_amount)
        trans_db.insert_transaction(dummy_transaction)

        running_date = self.start_date
        while running_date < self.end_date:
            # überprüfen ob datum ein börsenfreier tag ist
            day = db.get_day(running_date)
            raw_day_close = db.get_raw_day(running_date).close

            if day.close == -1:
                running_date += datetime.timedelta(days=1)
                continue

            avg200 = db.calc_average(running_date, 200)
            latest_transaction = trans_db.get_latest_transaction(running_date)

            # wenn an diesem tag ein split war
            if day.split != 1:
                latest_transaction.count *= day.split
                latest_transaction.id = None
                trans_db.insert_transaction(latest_transaction)

            # buy wenn 200-er schnitt den close wert überschreitet und letzte transaktion ein sale war und
            if avg200 < day.close and not latest_transaction.buy_flag:
                count = int(latest_transaction.depotkonto / decimal.Decimal(raw_day_close))
                depotkonto_remaining = latest_transaction.depotkonto - decimal.Decimal(count*raw_day_close)
                new_transaction = Transaction(running_date, self.symbol, True, count, depotkonto_remaining)
                trans_db.insert_transaction(new_transaction)

                print(new_transaction)

            # sell wenn 200-er schnitt den close unterschreitet und letzte transaktion ein buy war
            if avg200 > day.close and latest_transaction.buy_flag:
                depotkonto = latest_transaction.depotkonto + decimal.Decimal(raw_day_close * latest_transaction.count)
                new_transaction = Transaction(running_date, self.symbol, False, 0, depotkonto)
                trans_db.insert_transaction(new_transaction)

                print(new_transaction)

            running_date += datetime.timedelta(days=1)

            latest_transaction = trans_db.get_alltime_latest_transaction()
            self.roi = latest_transaction.depotkonto + \
                       decimal.Decimal(latest_transaction.count * db.get_closest_day(self.end_date).close)
            self.roi = float(self.roi)

        print_chart = input("Soll die Handels-Strategie Visualisiert werden? (y/n)\n")
        if print_chart.lower() == "y":
            display_200(trans_db.table_name, self.symbol)


if __name__ == "__main__":
    avg200 = AVG200Strat()
