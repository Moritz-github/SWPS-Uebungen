class DailyPrices:
    def __init__(self, datestring, open_value, high, low, close, volume, dividend, split):
        self.datestring = datestring
        self.open = float(open_value)
        self.high = float(high)
        self.low = float(low)
        self.close = float(close)
        self.volume = volume
        self.symbol = ""
        self.dividend = dividend
        self.split = split

    def __str__(self):
        return '''"Daily Prices of {}": {{
    "1. open": "{}",
    "2. high": "{}",
    "3. low": "{}",
    "4. close": "{}",
    "5. volume": "{}",
    "6. dividend": "{}",
    "7. split": "{}"
}}'''.format(self.datestring, self.open, self.high, self.low, self.close, self.volume, self.dividend, self.split)