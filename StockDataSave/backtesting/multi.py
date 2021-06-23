import datetime
from backtesting.avg_200 import AVG200Strat
from backtesting.buy_and_hold import BuyAndHold
from backtesting.database_transactions import TransactionsDBManager
import data_handler
from database import DBManager
import scrape
from backtesting.trading_strategy import DataNotInDataset
import decimal
import matplotlib.pyplot as plt

with open("backtest_config.txt") as f:
    lines = f.readlines()
lines = [x.strip() for x in lines]

invest_amount = float(lines.pop(0))
start_date = datetime.datetime.strptime(lines.pop(0), "%Y-%m-%d").date()
end_date = datetime.datetime.strptime(lines.pop(0), "%Y-%m-%d").date()
symbols = lines

invest_per_symbol = invest_amount / len(symbols)

tables_avg200 = []
tables_avg200_3 = []

values_BnH = {}
values_avg200 = {}
values_avg200_3 = {}

real_symbols = []

for symbol in symbols:
    db = DBManager(symbol)
    try:
        if not data_handler.scrape_and_save_raw_prices_to_db(db):
            data_handler.analyze_data_and_save_to_db(db)
        db.close()
    except scrape.SymbolNotFound:
        print("Symbol not Found - Skipping")
        continue

    try:
        buynhold = BuyAndHold(symbol=symbol, start_date=start_date, end_date=end_date, amount=invest_per_symbol)
        avg200 = AVG200Strat(percents=1.0, symbol=symbol, start_date=start_date, amount=invest_per_symbol, end_date=end_date)
        avg200_3 = AVG200Strat(percents=1.03, symbol=symbol, start_date=start_date, amount=invest_per_symbol, end_date=end_date)

        tables_avg200.append((symbol, avg200.table_name))
        tables_avg200_3.append((symbol, avg200_3.table_name))

        i = 0
        for day in buynhold.db.get_values(start_date, end_date):
            if day.datestring not in values_BnH.keys():
                values_BnH[day.datestring] = 0
            values_BnH[day.datestring] += buynhold.db.get_closest_raw_day(day.datestring).close * buynhold.trans_db.get_latest_transaction(day.datestring).count
            i+=1

        avg200.trans_db.close()
        avg200_3.trans_db.close()

        real_symbols.append(symbol)

    except DataNotInDataset:
            print("Data from start to end date is not in dataset - skipping")



fig, ax = plt.subplots()

ax.plot(values_BnH.keys(), values_BnH.values(), label="Buy and Hold")

avg_200_data = {}
avg_200_3_data = {}

def get_graph_data(symbol, table, dict):
    print(symbol, table)
    trans_db = TransactionsDBManager(symbol, table)
    db = DBManager(symbol)
    running_date = start_date
    while running_date < end_date:
        if running_date not in dict.keys():
            dict[running_date] = 0

        transaction = trans_db.get_latest_transaction(running_date)
        dict[running_date] += transaction.depotkonto + \
                                     transaction.count * decimal.Decimal(db.get_closest_raw_day(running_date).close)

        running_date += datetime.timedelta(days=1)


for symbol, table in tables_avg200:
    get_graph_data(symbol, table, avg_200_data)
for symbol, table in tables_avg200_3:
    get_graph_data(symbol, table, avg_200_3_data)

ax.plot(avg_200_data.keys(), avg_200_data.values(), label="AVG 200")
ax.plot(avg_200_3_data.keys(), avg_200_3_data.values(), label="AVG 200 +- 3%")

ax.set(xlabel="Date", ylabel="Value of all symbols summarised", title="comparison")
ax.grid()
fig.autofmt_xdate()

plt.legend()

plt.show()