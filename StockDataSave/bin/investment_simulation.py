import datetime
import database

symbol = input("Bei welcher Aktie wollen Sie ein Investment Simulieren? (z.B. Apple ... AAPL; Tesla ... TSLA; Amazon "
               "... AMZN)\n")

start_date = datetime.datetime.strptime(input('Investment-Datum (z.B. "2010-01-01"): '), "%Y-%m-%d").date()
end_date_input = input('Auszahl-Datum (falls bis heute -> enter): ')
if end_date_input != "":
    end_date = datetime.datetime.strptime(end_date_input, "%Y-%m-%d")
else:
    end_date = datetime.datetime.now().date()

investment_amount = float(input("Wie viele Euros sollen beim Anfangsdatum investiert werden?"))

db = database.DBManager(symbol)
start_dailyprice = db.get_closest_day(start_date)
end_dailyprice = db.get_closest_day(end_date)
print(start_dailyprice.datestring)

investment_return = investment_amount * (end_dailyprice.close / start_dailyprice.close)

print(f"Ein investment in {symbol} von {investment_amount:.0f}€ am {start_dailyprice.datestring} für {start_dailyprice.close:.2f}"
      f"€/Aktie,\nverkauft am {end_dailyprice.datestring} für {end_dailyprice.close:.2f}€/Aktie\nwären nun "
      f"{investment_return:.2f}€. (Rendiete: {(investment_return/investment_amount)*100 -100:.2f}%)")
