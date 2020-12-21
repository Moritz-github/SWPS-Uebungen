import database
import scrape

user_symbol = input("Bitte gib eine Aktie an (Apple ... AAPL; Tesla ... TSLA; Amazon ... AMZN)\n")

db = database.DBManager(user_symbol)
db.init_table()

prices = []

for daily_prices in scrape.get_daily_prices(user_symbol, outputsize="full"):
    db.add_row_from_daily_price(daily_prices)

    prices.append(daily_prices)

db.close()

print(f"Added {len(prices)} rows to the {user_symbol} table in the STOCKDATA database")

endlen = len(prices)-1
for i in range(endlen, endlen-100, -1):
    print(prices[i])
    print("200 Day Avg.: ", end="")
    twoHundredAVG = sum([x.close for x in prices[i-200:i]]) / 200
    print(twoHundredAVG)
    print("\n")