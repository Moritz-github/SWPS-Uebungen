import scrape


def scrape_and_save_raw_prices_to_db(db):
    compact_prices = scrape.get_daily_prices(db.symbol)
    if db.get_day((compact_prices[0]).datestring).close == -1:
        if db.get_day(compact_prices[-1].datestring).close == -1:
            print("More than 100 Days missing, downloading all data")

            prices = []

            for daily_prices in scrape.get_daily_prices(db.symbol, outputsize="full"):
                db.insert_raw(daily_prices)

                prices.append(daily_prices)
            print(f"Added {len(prices)} rows to the {db.symbol}_raw table in the database")
        else:
            print("Database not up to date, less than 100 days missing")
            for day in compact_prices:
                db.insert_raw(day)
    else:
        print("Database up to date")


def analyze_data_and_save_to_db(db):
    dailyprices = db.get_all_raw_values(desc=True)
    avg_values = []

    # Split correction
    for i in range(0, len(dailyprices)):
        splitvalue = float(dailyprices[i].split)
        if splitvalue != 0.0:
            for j in range(i+1, len(dailyprices)):
                dailyprices[j].open /= splitvalue
                dailyprices[j].high /= splitvalue
                dailyprices[j].low /= splitvalue
                dailyprices[j].close /= splitvalue

    # Write to DB
    for dailyprice in dailyprices:
        db.insert(dailyprice)

    # 200 AVG
    for dailyprice in dailyprices[:-200]:
        db.calc_average(dailyprice.datestring, 200)

    # Write to DB
    for dailyprice in dailyprices:
        db.insert(dailyprice)