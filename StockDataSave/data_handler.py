import scrape


def scrape_and_save_raw_prices_to_db(db):
    print("Downloading and saving prices to db")
    prices = []

    for daily_prices in scrape.get_daily_prices(db.symbol, outputsize="full"):
        db.insert_raw(daily_prices)

        prices.append(daily_prices)
    print(f"Added {len(prices)} rows to the {db.symbol} table in the database")


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
        dailyprice.avg200 = db.calc_200_average(dailyprice.datestring)

    # Write to DB
    for dailyprice in dailyprices:
        db.insert(dailyprice)