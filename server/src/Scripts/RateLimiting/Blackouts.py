import matplotlib.dates as md
import matplotlib.pyplot as plt
from dateutil import parser
from collections import OrderedDict
import numpy as np
import datetime
import json

tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]
for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)

# full_data_file = "gnip_hourly.json"
full_data_file= "RAW_A_TwitterBre_6f.json"
full_data = json.load(open(full_data_file))

brexit = None
for series in full_data["values"]:
    if series["_id"] == "ALL":
        brexit = series["data"]

print brexit[0]


start = parser.parse(full_data["categories"][0].rstrip("Z"))
end = parser.parse(full_data["categories"][-1].rstrip("Z"))
x_values = []
date = start
while date <= end:
    x_values.append(date)
    date += datetime.timedelta(hours=1)
full_c = OrderedDict([(parser.parse(i["dt"].rstrip("Z")),i["count"]) for i in brexit])

print x_values[0]
print full_c.items()[0]
print len(x_values)
print len(full_c)

full_counts = OrderedDict.fromkeys(x_values, 0)

for t in full_c.keys():
    full_counts[t] = full_c[t]

fig,ax = plt.subplots()


in_seg = False
edges = []
for n,i in enumerate(full_counts):
    if not in_seg and full_counts[i] == 0:
        edges.append(i)
        in_seg = True
    elif in_seg and full_counts[i] != 0:
        edges[-1] = (edges[-1],full_counts.keys()[n-1])
        in_seg = False

for i,j in edges:
    if(i!=j):
        plt.axvspan(i, j, color='y', alpha=0.5, lw=0)
        ax.text(j, 7000,
                (i + (i - j) / 2).strftime("%c") + " for " + str(float((j - i).total_seconds()) / (60 * 60)) + "hrs",
                fontsize=12,
                color="b", rotation=270)

plt.ylim([0, 8000])
ax.plot(full_counts.keys(), full_counts.values(), color=tableau20[10], label="Firehose", alpha = 0.5)
xfmt = md.DateFormatter("%a %d %b")
ax.xaxis.set_major_formatter(xfmt)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
plt.xlabel("Date UTC")
plt.ylabel("Tweet Rate /hour")

# plt.ion()
plt.show()
