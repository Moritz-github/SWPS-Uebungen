"""
API-Documentation: https://www.alphavantage.co/documentation

API Call Parameters
Functions:
TIME_SERIES_DAILY

Outputsize:
compact,
full

"""
import requests
import json
import database

user_symbol = input("Bitte gib eine Aktie an (Apple ... AAPL; Tesla ... TSLA)\n")

db = database.DBManager(user_symbol)

# Read API-Key from Text file
with open("api-key.txt") as file:
    api_key = file.readlines()[0]


class URLBuilder:
    def __init__(self, function, symbol, outputsize="compact", base_url="https://www.alphavantage.co/query?function={}&symbol={}&outputsize={}&apikey={}"):
        self.function = function
        self.symbol = symbol
        self.outputsize = outputsize
        self.base_url = base_url

    def __str__(self):
        return self.base_url.format(self.function, self.symbol, self.outputsize, api_key)


def request(url):
    return json.loads(requests.get(url).text)


def write_close_values_db(symbol):
    url = URLBuilder(function="TIME_SERIES_DAILY", symbol=symbol)
    response = request(url)
    days = response["Time Series (Daily)"]

    for day in days:
        close = days[day]["4. close"]
        db.add_value(day, float(close))

        # print("{}: Close: {}".format(day, close))


def get_close_values(symbol):
    url = URLBuilder(function="TIME_SERIES_DAILY", symbol=symbol)
    response = request(url)
    days = response["Time Series (Daily)"]

    for day in days:
        close = days[day]["4. close"]
        print("{}: Close: {}".format(day, close))


print(write_close_values_db(user_symbol))