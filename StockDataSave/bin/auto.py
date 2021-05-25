import database
import data_handler
import plotting
import datetime

with open("../config/config.txt") as file:
    lines = file.readlines()
    start_date = lines.pop(0).strip()
    end_date = lines.pop(0).strip()
    avg = int(lines.pop(0).strip())
    symbols = []
    while len(lines) != 0:
        symbols.append(lines.pop(0).strip())

for symbol in symbols:
    db = database.DBManager(symbol)

    if not data_handler.scrape_and_save_raw_prices_to_db(db):
        print("Analyzing data")
        data_handler.analyze_data_and_save_to_db(db)

    filename = "charts\\{}-{}.png".format(symbol, datetime.datetime.now().strftime("%d-%m-%Y"))
    plotting.create_chart(start_date, end_date, db, filename)
