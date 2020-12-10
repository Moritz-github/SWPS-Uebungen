import database
import scrape

user_symbol = input("Bitte gib eine Aktie an (Apple ... AAPL; Tesla ... TSLA; Amazon ... AMZN)\n")

db = database.DBManager(user_symbol)
db.init_table()

count = 0
for daily_prices in scrape.get_daily_prices(user_symbol, outputsize="full"):
    db.add_row_from_daily_price(daily_prices)
    count += 1
print(f"Added {count} rows to the {user_symbol} table in the STOCKDATA database")

db.close()