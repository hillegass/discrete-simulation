import sys
import datetime

def str_for_day(day):
    delta = datetime.timedelta(days=day)
    d = datetime.date.today() + delta
    return d.strftime('%b %d, %Y')