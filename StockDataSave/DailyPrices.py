class DailyPrices:
    def __init__(self, datestring, open_value, high, low, close, volume):
        self.datestring = datestring
        self.open = float(open_value)
        self.high = float(high)
        self.low = float(low)
        self.close = float(close)
        self.volume = volume

    def __str__(self):
        return '''"Daily Prices of {}": {{
    "1. open": "{}",
    "2. high": "{}",
    "3. low": "{}",
    "4. close": "{}",
    "5. volume": "{}"
}}'''.format(self.datestring, self.open, self.high, self.low, self.close, self.volume)