import requests
from datetime import datetime
weekdays_off = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
for year in [requests.get("https://feiertage-api.de/api/?jahr={}&nur_land=BY".format(str(x))).json() for x in range(2020, 2031)]:
    for feiertag_name in year:
        weekdays_off[datetime.strptime(year[feiertag_name]["datum"], "%Y-%m-%d").weekday()] += 1
[print(str(day+1)+ ": " + str(weekdays_off[day])) for day in weekdays_off]
