import calendar
from datetime import date

WEEKDAYS_FR = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]

def get_days_in_month(year, month):
    _, last_day = calendar.monthrange(year, month)
    days = []
    for d in range(1, last_day + 1):
        dt = date(year, month, d)
        days.append({
            "day": d,
            "weekday": WEEKDAYS_FR[dt.weekday()],
            "date": dt
        })
    return days

def get_weekday_fr(dt):
    return WEEKDAYS_FR[dt.weekday()]
