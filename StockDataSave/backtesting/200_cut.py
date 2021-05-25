import datetime
import decimal
import database
from backtesting import database_transactions
from backtesting.transaction import Transaction

# https://pyinvesting.com/backtest/moving-average/moving-average-preview/amzn/Simple/200

symbol = input("Bei welcher Aktie wollen Sie ein Investment Simulieren? (z.B. Apple ... AAPL; Tesla ... TSLA; Amazon "
               "... AMZN)\n")
invest_date = datetime.datetime.strptime(input('Investment-Datum (z.B. "2010-01-01"): '), "%Y-%m-%d").date()
end_date_input = input('Auszahl-Datum (falls bis heute -> enter): ')
invest_amount = float(input("Wie viel Geld soll Investiert werden?"))

if end_date_input != "":
    end_date = datetime.datetime.strptime(end_date_input, "%Y-%m-%d")
else:
    end_date = datetime.datetime.now().date()

trans_db = database_transactions.TransactionsDBManager(symbol)
db = database.DBManager(symbol)

dummy_transaction = Transaction(invest_date, "DUMMY", False, 0, invest_amount)
trans_db.insert_transaction(dummy_transaction)

points = []

start_date = invest_date
while start_date < end_date:
    # überprüfen ob datum ein börsenfreier tag ist
    day = db.get_day(start_date)
    raw_day_close = db.get_raw_day(start_date).close

    if day.close == -1:
        start_date += datetime.timedelta(days=1)
        continue

    avg200 = db.calc_average(start_date, 200)
    latest_transaction = trans_db.get_latest_transaction(start_date)

    # wenn an diesem tag ein split war
    if day.split != 1:
        latest_transaction.count *= day.split
        latest_transaction.id = None
        trans_db.insert_transaction(latest_transaction)

    # buy wenn 200-er schnitt den close wert überschreitet und letzte transaktion ein sale war und
    if avg200 < day.close and not latest_transaction.buy_flag:
        count = int(latest_transaction.depotkonto / decimal.Decimal(raw_day_close))
        depotkonto_remaining = latest_transaction.depotkonto - decimal.Decimal(count*raw_day_close)
        new_transaction = Transaction(start_date, symbol, True, count, depotkonto_remaining)
        trans_db.insert_transaction(new_transaction)

        points.append(day.datestring)

    # sell wenn 200-er schnitt den close unterschreitet und letzte transaktion ein buy war
    if avg200 > day.close and latest_transaction.buy_flag:
        depotkonto = latest_transaction.depotkonto + decimal.Decimal(raw_day_close * latest_transaction.count)
        new_transaction = Transaction(start_date, symbol, False, 0, depotkonto)
        trans_db.insert_transaction(new_transaction)

        points.append(day.datestring)

    start_date += datetime.timedelta(days=1)

latest_transaction = trans_db.get_alltime_latest_transaction()
rendite = latest_transaction.depotkonto + decimal.Decimal(latest_transaction.count * db.get_closest_day(end_date).close)
# print("Die Ursprünglich investierten {}€ sind nun {}€".format(invest_amount, rendite))
print(f"Die Ursprünglich investierten {invest_amount}€ sind nun {rendite:.2f}€")