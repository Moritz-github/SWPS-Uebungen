import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, date


def create_chart(start_date, end_date, db, filename=""):
    data = db.get_values(start_date, end_date)
    dates = [x.datestring for x in data]
    closes = [x.close for x in data]
    avg200s = [db.calc_average(x.datestring, 200) for x in data]

    fig, ax = plt.subplots()
    ax.plot(dates, closes, label="Close Values")
    ax.plot(dates, avg200s, label="200 Averages")

    ax.set(xlabel="Date", ylabel="Close value adjusted", title=db.symbol)
    ax.grid()
    fig.autofmt_xdate()

    if closes[1] > avg200s[1]:
        ax.set_facecolor((.1, .5, .1, .4))
    else:
        ax.set_facecolor((.5,.1,.1, .6))

    plt.legend()
    if filename == "":
        plt.show()
    else:
        plt.savefig(filename)