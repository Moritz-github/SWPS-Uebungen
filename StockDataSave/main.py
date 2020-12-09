import database
import scrape

user_symbol = input("Bitte gib eine Aktie an (Apple ... AAPL; Tesla ... TSLA)\n")

for day in scrape.get_close_values(user_symbol):
    print(day)