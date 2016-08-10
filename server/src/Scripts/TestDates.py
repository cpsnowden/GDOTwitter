import datetime
import json
from dateutil import parser

path =  "/Users/ChrisSnowden/IndividualProject/GDOTwitter/DATA/RAW_A_TwitterBre_64.json"
with open(path) as f:
    data = json.load(f)


data = data["data"]
x_categories = [parser.parse(i) for i in data["categories"]]


def get_time_values(start, end, interval):
    t_values = []
    date = start
    while date <= end:
        t_values.append(date)
        date += datetime.timedelta(**{interval.lower() + "s": 1})

    return t_values

import pprint

full = get_time_values(x_categories[0], x_categories[-1], "minute")
print len(full)
print len(x_categories)
# pprint.pprint()

for i in x_categories:
    if i not in full:
        print "Not found"
