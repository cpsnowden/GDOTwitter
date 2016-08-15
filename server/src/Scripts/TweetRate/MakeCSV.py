import csv
import json
from dateutil import  parser


raw = json.load(open("brexit.json"))

with open("brexit.csv","w") as f:
    writer = csv.writer(f, quotechar = "'")
    writer.writerow(['\"\"','\"timestamp\"','\"count\"'])
    for i,entry in enumerate(raw):
        writer.writerow(['\"' + str(i) + '\"', parser.parse(entry[0]).strftime("%Y-%m-%d %H:%M:%S"), entry[1]])