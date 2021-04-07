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
    daily_prices = []
    for day in days:
        values = days[day]
        open = values["1. open"]
        high = values["2. high"]
        low = values["3. low"]
        close = values["4. close"]
        volume = values["6. volume"]
        dividend = values["7. dividend amount"]
        split = values["8. split coefficient"]

        daily_prices.append(DailyPrices(day, open, high, low, close, volume, dividend, split))
    return daily_prices
