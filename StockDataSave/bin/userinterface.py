from datetime import datetime
import database
import plotting
import data_handler
import scrape


symbol = input("Bitte gib eine Aktie an (z.B. Apple ... AAPL; Tesla ... TSLA; Amazon ... AMZN)\n")

db = database.DBManager(symbol)

data_handler.scrape_and_save_raw_prices_to_db(db)
print("Analyzing data")
data_handler.analyze_data_and_save_to_db(db)

start_date = datetime.strptime(input("Start-Datum (z.B.: 31-12-2010): "), "%d-%m-%Y").date()
end_date = datetime.strptime(input("End-Datum (z.B.: 31-12-2020): "), "%d-%m-%Y").date()

plotting.create_chart(start_date, end_date, db)

save_file = input('Soll dieser Chart als Bild abgespeichert werden? ("y"/"n")')
if save_file == "y":
    filename = "charts\\{}-{}.png".format(symbol, datetime.now().strftime("%d-%m-%Y"))
    plotting.create_chart(start_date, end_date, db, filename)
