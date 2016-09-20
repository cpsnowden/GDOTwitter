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

sample_data_file = "sampled.dat"
full_data_file = "gnip.json"

full_data = json.load(open(full_data_file))
sample_data = json.load(open(sample_data_file))

x_values = sorted([parser.parse(i) for i in  sample_data["brexit"].keys()])
sample_c = dict([(parser.parse(i),c) for (i,c) in sample_data["brexit"].iteritems()])

brexit = None
for series in full_data["data"]["values"]:
    if series["_id"] == "brexit":
        brexit = series["data"]

full_c = dict([(parser.parse(i["dt"]),i["count"]) for i in brexit[-12000:] if parser.parse(i["dt"]) >= min(x_values)])


sampled_counts = OrderedDict.fromkeys(x_values, 0)
full_counts = OrderedDict.fromkeys(x_values, 0)

for t in x_values:
    sampled_counts[t] = sample_c[t]
    full_counts[t] = full_c[t]

fig,ax = plt.subplots(nrows=2)


ax[0].plot(x_values, sampled_counts.values(), color = tableau20[0], label ="StreamingAPI")
ax[0].plot(x_values, full_counts.values(), color=tableau20[10], label="Firehose")
ax[0].spines["top"].set_visible(False)
ax[0].spines["right"].set_visible(False)
ax[0].get_xaxis().tick_bottom()
ax[0].get_yaxis().tick_left()
ax[0].set_xticks([])
ax[0].legend()
ax[0].set_ylabel("Tweet Rate /min", fontsize = 14)
fontsize = 14
# ax[0].tick_params(axis='x', labelsize=fontsize)
ax[0].yaxis.set_ticks(xrange(0, 11000, 2000))
ax[0].tick_params(axis='y', labelsize=fontsize)

ax[1].plot(x_values, np.array(sampled_counts.values()).astype(float) / np.array(full_counts.values()) * 100,
           color = tableau20[0])
ax[1].plot([min(x_values), max(x_values)], [100,100], "--", lw=0.5, color="black", alpha=0.3)
xfmt = md.DateFormatter("%a %H:%M")
ax[1].xaxis.set_major_formatter(xfmt)
ax[1].spines["top"].set_visible(False)
ax[1].spines["right"].set_visible(False)
ax[1].get_xaxis().tick_bottom()
ax[1].get_yaxis().tick_left()



ax[1].tick_params(axis='x', labelsize=fontsize)
ax[1].tick_params(axis='y', labelsize=fontsize)
plt.xlabel("Date UTC", fontsize = 14)
plt.ylim([0, 110])
plt.ylabel("Coverage /%", fontsize = 14)

plt.show()