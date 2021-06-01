from backtesting import database_transactions
import database
import plotting

def display_200(table, symbol):
    db_trans = database_transactions.TransactionsDBManager(symbol, table)
    db = database.DBManager(symbol)

    transactions = db_trans.get_all_transactions()
    for x in transactions:
        print(x)
    points = [x.date for x in transactions if x.symbol != "DUMMY"]

    values = db.get_all_values()

    # if last action was a buy, we need to add a point to the last date for the chart to mark the last buy until now
    if transactions[-1].buy_flag == 1:
        points.append(values[-1].datestring)

    plotting.create_chart("2005-01-01", "2021-05-25", db, points=points)


if __name__ == "__main__":
    table = "backtest 19:56:55 01-06-2021"
    symbol = "IBM"
    display_200(table, symbol)