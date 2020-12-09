import requests
import json
from URLBuilder import URLBuilder


def send_request_and_json(url):
    return json.loads(requests.get(url).text)


def get_close_values(symbol):
    url = URLBuilder(function="TIME_SERIES_DAILY", symbol=symbol)
    response = send_request_and_json(url)
    days = response["Time Series (Daily)"]

    for day in days:
        close = days[day]["4. close"]
        yield day, float(close)
