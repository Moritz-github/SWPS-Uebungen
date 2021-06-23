import requests
import json
from URLBuilder import URLBuilder
from DailyPrices import DailyPrices
from pprint import pprint
import time

class APIFrequency(Exception):
    def __init__(self, message="The ALPHAVANTAGE API allows max 5 requests/minute. Waiting 1 minute."):
        super().__init__(message)

class SymbolNotFound(Exception):
    def __init__(self, message="Symbol not Found!"):
        super().__init__(message)


def send_request_get_json(url):
    text = requests.get(url).text
    if "Our standard API call frequency is 5 calls per minute and 500 calls per day" in text:
        raise APIFrequency
    if "Invalid API call." in text:
        raise SymbolNotFound
    return json.loads(text)


def get_daily_prices(symbol, function="TIME_SERIES_DAILY_ADJUSTED", outputsize="compact"):
    url = URLBuilder(function=function, symbol=symbol, outputsize=outputsize)
    print("Sending request to {}".format(url))
    while True:
        try:
            response = send_request_get_json(url)
            break
        except APIFrequency:
            print("API Frequency error. Wating 10 secs")
            time.sleep(10)
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
