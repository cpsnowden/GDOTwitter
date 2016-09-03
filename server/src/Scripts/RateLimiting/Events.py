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

# sample_data_file = "sampled.dat"
full_data_file = "gnip.json"

full_data = json.load(open(full_data_file))
# sample_data = json.load(open(sample_data_file))

# x_values = sorted([parser.parse(i) for i in  sample_data["brexit"].keys()])
# sample_c = dict([(parser.parse(i),c) for (i,c) in sample_data["brexit"].iteritems()])

brexit = None
for series in full_data["data"]["values"]:
    if series["_id"] == "brexit":
        brexit = series["data"]

full_c = dict([(parser.parse(i["dt"]), i["count"]) for i in brexit[-12000:]])

# sampled_counts = OrderedDict.fromkeys(x_values, 0)
x_values = sorted(full_c.keys())
full_counts = OrderedDict.fromkeys(x_values, 0)

for t in x_values:
    # sampled_counts[t] = sample_c[t]
    full_counts[t] = full_c[t]

fig, ax = plt.subplots()

# ax.plot(x_values, sampled_counts.values(), color = tableau20[0], label ="StreamingAPI")
ax.plot(x_values, full_counts.values(), color=tableau20[10], label="Firehose")
xfmt = md.DateFormatter('%Y-%m-%d\n %H:%M:%S')
ax.xaxis.set_major_formatter(xfmt)

start_date = datetime.datetime(2016, 06, 23, 20)
end_date = datetime.datetime(2016, 06, 24, 10)

polls_close = datetime.datetime(2016, 06, 23, 21)
first_results = datetime.datetime(2016, 06, 23, 22, 38)
leave_lead = datetime.datetime(2016, 06, 23, 23, 17)
nigel = datetime.datetime(2016, 06, 24, 03, 02)
forecast = datetime.datetime(2016, 06, 24, 03, 36)
win = datetime.datetime(2016, 06, 24, 05)
dc = datetime.datetime(2016, 06, 24, 7, 23)

top = 10000
ano = 9000

ax.plot((polls_close, polls_close), (0, ano), "--", color="black", alpha=0.3)
ax.plot((first_results, first_results), (0, ano), "--", color="black", alpha=0.3)
ax.plot((leave_lead, leave_lead), (0, ano), "--", color="black", alpha=0.3)
ax.plot((nigel, nigel), (0, ano), "--", color="black", alpha=0.3)
ax.plot((forecast, forecast), (0, ano), "--", color="black", alpha=0.3)
ax.plot((win, win), (0, ano), "--", color="black", alpha=0.3)
ax.plot((dc, dc), (0, ano), "--", color="black", alpha=0.3)

ax.text(polls_close, ano, "A",
        ha="center",
        size=12,
        bbox=dict(boxstyle="circle", fc="w", ec="k"))

ax.text(first_results, ano, "B",
        ha="center",
        size=12,
        bbox=dict(boxstyle="circle", fc="w", ec="k"))

ax.text(leave_lead, ano, "C",
        ha="center",
        size=12,
        bbox=dict(boxstyle="circle", fc="w", ec="k"))

ax.text(nigel, ano, "D",
        ha="center",
        size=12,
        bbox=dict(boxstyle="circle", fc="w", ec="k"))

ax.text(forecast, ano, "E",
        ha="center",
        size=12,
        bbox=dict(boxstyle="circle", fc="w", ec="k"))

ax.text(win, ano, "F",
        ha="center",
        size=12,
        bbox=dict(boxstyle="circle", fc="w", ec="k"))

ax.text(dc, ano, "G",
        ha="center",
        size=12,
        bbox=dict(boxstyle="circle", fc="w", ec="k"))

plt.xlim([start_date, end_date])

dates = [
    datetime.datetime(2016, 06, 23, 20),
    datetime.datetime(2016, 06, 23, 22),
    datetime.datetime(2016, 06, 24, 00),
    datetime.datetime(2016, 06, 24, 2),
    datetime.datetime(2016, 06, 24,4),
    datetime.datetime(2016, 06, 24,6),
    datetime.datetime(2016, 06, 24,8),
    datetime.datetime(2016, 06, 24,10)
]
plt.xticks(dates, [i.strftime("%a %d %b \n%H:%M") for i in dates])
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
plt.xlabel("Date UTC")
plt.ylabel("Tweet Rate /min")

plt.show()
