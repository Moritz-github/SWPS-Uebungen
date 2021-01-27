import requests
import json
from URLBuilder import URLBuilder
from DailyPrices import DailyPrices
from pprint import pprint


def send_request_get_json(url):
    return json.loads(requests.get(url).text)


def get_daily_prices(symbol, function="TIME_SERIES_DAILY_ADJUSTED", outputsize="compact"):
    url = URLBuilder(function=function, symbol=symbol, outputsize=outputsize)
    print("Sending request to {}".format(url))
    response = send_request_get_json(url)
    days = response["Time Series (Daily)"]
    for day in days:
        open = days[day]["1. open"]
        high = days[day]["2. high"]
        low = days[day]["3. low"]
        close = days[day]["4. close"]
        volume = days[day]["6. volume"]

        yield DailyPrices(day, open, high, low, close, volume)
