tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]
for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)
import matplotlib.dates as md
import json
from collections import OrderedDict
from dateutil import parser
import datetime

path = "RAW_A_TwitterBre_40e5a45.json"
with open(path) as f:
    data = json.load(f)

x_categories = [parser.parse(i) for i in data["categories"]]
y_labels = OrderedDict.fromkeys(x_categories, 0)

import matplotlib.pyplot as plt
fig,ax = plt.subplots()

def s(x):
    return sum([i["count"] for i in x["data"]])

v = sorted(data["values"], key = s, reverse=True)
print [i["_id"] for i in v]
j  = 0
for i,series in enumerate(v[:11]):
    if series["_id"] == "Unspecified":
        continue
    for entry in series["data"]:
        y_labels[parser.parse(entry["dt"])] = entry["count"]

    l = ax.plot(x_categories, list(y_labels.values()), label=series["_id"], color=tableau20[j])
    j += 1

    y_labels = OrderedDict.fromkeys(x_categories, 0)

xfmt = md.DateFormatter("%a %H:%M")

ax.xaxis.set_major_formatter(xfmt)
ax.set_ylabel("Tweet Rate thousand/hour", fontsize = 14)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
ax.tick_params(axis='x', labelsize=14)
# ax[0].yaxis.set_ticks(xrange(0, 11000, 2000))
ax.tick_params(axis='y', labelsize=14)
plt.legend(bbox_to_anchor=(0., 0.9, 0.6, .102), loc=2, ncol=5, mode="expand", borderaxespad=0., frameon=True)
plt.yticks(xrange(0,140001,20000), xrange(0,141,20))
start = datetime.datetime(2016,6,20)
end = datetime.datetime(2016,6,27)
plt.xlim([start, end])
plt.show()