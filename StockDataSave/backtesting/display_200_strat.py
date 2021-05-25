from backtesting import database_transactions
import database
import plotting

table = "backtest 20:53:39 05-05-2021"
symbol = "AMZN"

db_trans = database_transactions.TransactionsDBManager(symbol, table)
db = database.DBManager(symbol)

transactions = db_trans.get_all_transactions()
points = [x.date for x in transactions]

values = db.get_all_values()
plotting.create_chart("2010-01-01", "2021-05-25", db, points=points)
