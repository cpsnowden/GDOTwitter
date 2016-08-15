from dateutil import parser
from collections import OrderedDict
# import matplotlib.pyplot as plt
import json
# import mpld3
# import matplotlib.dates as md
dpi = 1

tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]
for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)

with open(path) as f:
    data = json.load(f)

for i,series in enumerate(data["values"]):
    for entry in series["data"]:
        y_labels[parser.parse(entry["dt"])] = entry["count"]
    # l = ax.plot(x_categories, list(y_labels.values()), label=series["_id"], color = tableau20[i])
    if series["_id"] == "voteleave":
        leave = y_labels
        break
    if series["_id"] != "voteleave":
        continue
    # elif series["_id"]=="voteremain":
    #     remain = y_labels
    # elif series["_id"] == "brexit":
    #     brexit = y_labels
    y_labels = OrderedDict.fromkeys(x_categories, 0)
