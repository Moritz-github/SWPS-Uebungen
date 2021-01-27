import matplotlib.pyplot as plt
from datetime import datetime, timedelta


def plot_chart(days_count, db, user_symbol):
    avg_values = []
    values = []
    x_axis = []

    i = 0
    while len(avg_values) < days_count:
        day = datetime.now() - timedelta(days=i)
        j = db.get_200_average(day)
        if j is not None:
            avg_values.append(j)
            values.append(db.get_day(day))
            x_axis.append(day)
        i += 1

    ax = plt.axes()

    if values[1] > avg_values[1]:
        ax.set_facecolor((.1, .5, .1, .4))
    else:
        ax.set_facecolor((.5,.1,.1, .6))

    plt.style.use("seaborn")
    plt.plot(x_axis, values, label="Close Values")
    plt.plot(x_axis, avg_values, "b--", label="200 AVG")
    plt.xlabel("DATE")
    plt.ylabel("$ Price")
    plt.title("{} Stock Price".format(user_symbol.upper()))
    plt.legend()
    plt.show()