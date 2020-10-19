import requests
from datetime import datetime
from datetime import timedelta

state = "BY"
startyear = 2020
endyear = 2021

class apiHandler():
    def __init__(self, days_off_url="https://feiertage-api.de/api/?jahr={}&nur_land={}",
                 school_holidays_url="https://ferien-api.de/api/v1/holidays/{}/{}"):
        self.days_off_url = days_off_url
        self.school_holidays_url = school_holidays_url

    def get_days_off_one_year(self, year):
        a = requests.get(self.days_off_url.format(str(year), str(state))).json()
        print(a)
        return a

    def get_days_off_year_range(self, startyear, endyear):
        return [self.get_days_off_one_year(x) for x in range(startyear, endyear)]

    def get_school_holidays_of_one_year(self, year):
        return requests.get(self.school_holidays_url.format(str(state), str(year))).json()

    def get_school_holidays_of_year_range(self, startyear, endyear):
        return [self.get_school_holidays_of_one_year(x) for x in range(startyear, endyear)]


api = apiHandler()
feiertage = []
ferientage = []

# Alle Feiertage in die feiertage liste hinzufügen
for year in api.get_days_off_year_range(startyear, endyear):
    for feiertag_name in year:
        date = datetime.strptime(year[feiertag_name]["datum"], "%Y-%m-%d")
        feiertage.append(date)

# Alle Ferien in die Ferien liste hinzufügen
for year in api.get_school_holidays_of_year_range(startyear, endyear):
    for ferien_einheit in year:
        start_date = datetime.strptime(ferien_einheit["start"], "%Y-%m-%dT%M:%SZ")
        end_date =datetime.strptime(ferien_einheit["end"], "%Y-%m-%dT%M:%SZ")
        while start_date <= end_date:
            # print(start_date)
            ferientage.append(start_date)
            start_date += timedelta(days=1)

# Freien Tage Mergen
alle_freien_tage = feiertage + list(set(ferientage) - set(feiertage))
wochentage_dict = {0: "Montag", 1:"Dienstag", 2:"Mittwoch", 3:"Donnerstag", 4:"Freitag", 5:"Samstag", 6:"Sonntag"}
freie_wochentage = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0}

for feiertag in feiertage:
    if feiertag in ferientage:
        continue
    if feiertag.weekday() in (5,6):
        continue
    print(feiertag)
    freie_wochentage[feiertag.weekday()] += 1

for wochentag in freie_wochentage:
    print(wochentage_dict[wochentag] + ": " + str(freie_wochentage[wochentag]))
