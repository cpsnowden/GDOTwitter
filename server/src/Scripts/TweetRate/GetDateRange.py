from dateutil import parser
import datetime
import json

first = "2016-01-06T16:00:00"
last = "2016-06-30T23:00:00"

first_date = parser.parse(first)
last_date = parser.parse(last)


date = first_date
dates = [date]
while date <= last_date:
    date += datetime.timedelta(hours=1)
    dates.append(date)

print len(dates)
json.dump(dates, open("dates.json","w"), default=lambda obj: (obj.isoformat() + "Z"  if isinstance(obj,
                                                                                                   datetime.datetime)
                                                              else None))