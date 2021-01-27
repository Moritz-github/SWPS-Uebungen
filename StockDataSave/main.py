import database
import scrape
import plotting


def scrape_and_save_prices_to_db(user_symbol, db):
    prices = []

    for daily_prices in scrape.get_daily_prices(user_symbol, outputsize="full"):
        db.add_row_from_daily_price(daily_prices)

        prices.append(daily_prices)
    print(f"Added {len(prices)} rows to the {user_symbol} table in the STOCKDATA database")


nav = input("Was wollen Sie machen?\n1 ... Aktie Darstellen\n")

if nav == "1":
    user_symbol = input("Bitte gib eine Aktie an (z.B. Apple ... AAPL; Tesla ... TSLA; Amazon ... AMZN)\n")

    db = database.DBManager(user_symbol)
    db.open()

    if not db.check_if_table_exists():
        while True:
            nav = input(
                "Diese Aktie wurde nicht in der Datenbank gefunden. Jetzt herunterladen und in Datenbank speichern? ("
                "y/n)\n")
            if nav in ("y", "n"):
                break
            else:
                print("Bitte gib entweder 'y' oder 'n' an.")

        if nav == "y":
            db.init_table()
            scrape_and_save_prices_to_db(user_symbol, db)
        elif nav == "n":
            exit()

    days_count = int(input("Wie viele Tage in die Vergangenheit sollen dargestellt werden?\n"))
    plotting.plot_chart(days_count, db, user_symbol)

    db.close()
