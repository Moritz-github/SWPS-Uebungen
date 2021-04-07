import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, date


def create_chart(start_date, end_date, db, filename=""):
    data = db.get_values(start_date, end_date)
    print(data[0])
    dates = [x.datestring for x in data]
    closes = [x.close for x in data]
    avg200s = [x.avg200 for x in data]

    fig, ax = plt.subplots()
    ax.plot(dates, closes, label="Close Values")
    ax.plot(dates, avg200s, label="200 Averages")

    ax.set(xlabel="Date", ylabel="Close value adjusted", title=db.symbol)
    ax.grid()
    fig.autofmt_xdate()

    plt.legend()
    if filename == "":
        plt.show()
    else:
        plt.savefig(filename)