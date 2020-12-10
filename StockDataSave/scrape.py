import requests
import json
from URLBuilder import URLBuilder
from DailyPrices import DailyPrices


def send_request_get_json(url):
    return json.loads(requests.get(url).text)


def get_daily_prices(symbol, function="TIME_SERIES_DAILY", outputsize="compact"):
    url = URLBuilder(function=function, symbol=symbol, outputsize=outputsize)
    response = send_request_get_json(url)
    days = response["Time Series (Daily)"]
    print(url)

    for day in days:
        open = days[day]["1. open"]
        high = days[day]["2. high"]
        low = days[day]["3. low"]
        close = days[day]["4. close"]
        volume = days[day]["5. volume"]

        yield DailyPrices(day, open, high, low, close, volume)
