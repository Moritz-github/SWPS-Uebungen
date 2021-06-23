import datetime
import decimal
import database
from backtesting import database_transactions
from backtesting.transaction import Transaction
from backtesting.display_200_strat import display_200
from backtesting.trading_strategy import TradingStrategy

# https://pyinvesting.com/backtest/moving-average/moving-average-preview/amzn/Simple/200


class AVG200Strat(TradingStrategy):
    def __init__(self, percents=1.0, symbol=None, start_date=None, end_date=None, amount=None):
        self.percents = percents
        super().__init__(symbol=symbol, start_date=start_date, end_date=end_date, amount=amount)


        if amount is None:
            print_chart = input("Soll die Handels-Strategie Visualisiert werden? (y/n)\n")
            if print_chart.lower() == "y":
                display_200(self.table_name, self.symbol)


    def set_name(self):
        self.name = f"200-er Schnitt +/-{self.percents*100-100:.2f}%"

    def simulate_strategy(self):

        self.db = database.DBManager(self.symbol)

        dummy_transaction = Transaction(self.start_date, "DUMMY", False, 0, self.investment_amount)
        self.trans_db.insert_transaction(dummy_transaction)

        days = self.db.get_all_values()
        days_dict = {}
        for day in days:
            days_dict[day.datestring] = day


        days_raw_dict = {}
        days_raw = self.db.get_all_raw_values()
        for day in days_raw:
            days_raw_dict[day.datestring] = day

        latest_transaction = dummy_transaction
        running_date = self.start_date
        while running_date < self.end_date:
            # überprüfen ob datum ein börsenfreier tag ist
            if running_date not in days_dict.keys():
                running_date += datetime.timedelta(days=1)
                continue

            day = days_dict[running_date]
            raw_day_close = days_raw_dict[running_date].close

            avg200 = self.db.calc_average(running_date, 200)

            # wenn an diesem tag ein split war
            if day.split != 1:
                latest_transaction.count *= day.split
                latest_transaction.id = None
                self.trans_db.insert_transaction(latest_transaction)

            # buy wenn 200-er schnitt den close wert überschreitet und letzte transaktion ein sale war und
            if float(avg200) * self.percents < day.close and not latest_transaction.buy_flag:
                count = int(decimal.Decimal(latest_transaction.depotkonto) / decimal.Decimal(raw_day_close))
                depotkonto_remaining = decimal.Decimal(latest_transaction.depotkonto) - decimal.Decimal(count*raw_day_close)
                new_transaction = Transaction(running_date, self.symbol, True, count, depotkonto_remaining)
                self.trans_db.insert_transaction(new_transaction)
                latest_transaction = new_transaction
                # print(new_transaction)

            # sell wenn 200-er schnitt den close unterschreitet und letzte transaktion ein buy war
            if float(avg200) > float(day.close) * self.percents  and latest_transaction.buy_flag:
                depotkonto = decimal.Decimal(latest_transaction.depotkonto) + decimal.Decimal(decimal.Decimal(raw_day_close) * latest_transaction.count)
                new_transaction = Transaction(running_date, self.symbol, False, 0, depotkonto)
                self.trans_db.insert_transaction(new_transaction)
                latest_transaction = new_transaction

                # print(new_transaction)

            running_date += datetime.timedelta(days=1)

        latest_transaction = self.trans_db.get_alltime_latest_transaction()
        self.roi = latest_transaction.depotkonto + \
                   decimal.Decimal(latest_transaction.count * self.db.get_closest_day(self.end_date).close)
        self.roi = float(self.roi)

        self.table_name = self.trans_db.table_name

        self.db.close()
        # self.trans_db.close()


if __name__ == "__main__":
    avg200 = AVG200Strat(1.0)
