import matplotlib.pyplot as plt
import json
import numpy as np
import matplotlib.dates as md
from dateutil import parser
path = "/Users/ChrisSnowden/Downloads/A_Brexitold_e45.json"

data = json.load(open(path))
dataseries = data["data"]
datasets = dataseries.keys()
# print datasets

series = []
for s_name in datasets:
    if "_neg" in s_name:
        name = s_name[:-4]
        series.append(name)
ax = plt.subplot(111)
xfmt = md.DateFormatter('%Y-%m-%d\n %H:%M:%S')
ax.xaxis.set_major_formatter(xfmt)
time = [parser.parse(i) for i in dataseries[series[0]+"_pos"].keys()]
for s in series:
    positive = dataseries[s+"_pos"]
    negative = dataseries[s + "_neg"]
    values = -np.divide(np.array(positive.values(), dtype=float),np.array(negative.values(), dtype=float))
    values[~ np.isfinite(values)] = 0
    values = [x for (y,x) in sorted(zip(time,values))]

    ax.plot(sorted(time), values, label = s)
plt.legend()
plt.show()

