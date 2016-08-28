from dateutil import parser
from collections import OrderedDict
import matplotlib.dates as md
import matplotlib.pyplot as plt
import mpld3
import json
dpi = 1
import datetime
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]
for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)

path =  "/Users/ChrisSnowden/IndividualProject/GDOTwitter/DATA/RAW_A_TwitterBre_hourly.json"
with open(path) as f:
    data = json.load(f)


data = data["data"]

x_categories = [parser.parse(i) for i in data["categories"]]
y_labels = OrderedDict.fromkeys(x_categories, 0)

# fig = plt.figure(figsize=(1920 / dpi, 1080 / dpi), dpi=dpi, )
fig,ax = plt.subplots()
import copy

for i,series in enumerate(data["values"]):
    # if series["_id"] != "brexit":
    #     continue
    for entry in series["data"]:
        y_labels[parser.parse(entry["dt"])] = entry["count"]
    if series["_id"] != "brexit":
        continue
    l = ax.plot(x_categories, list(y_labels.values()), label=series["_id"], color=tableau20[i])


    # if series["_id"] == "voteleave":
    #     leave = copy.deepcopy(y_labels)
    # elif series["_id"]=="strongerin":
    #     remain = copy.deepcopy(y_labels)
    y_labels = OrderedDict.fromkeys(x_categories, 0)

xfmt = md.DateFormatter('%Y-%m-%d\n %H:%M:%S')

# json.dump(leave.items(), open("leave.json","w"), default=lambda obj: (obj.isoformat()  if isinstance(obj,
#                                                                                                   datetime.datetime) else None))
# json.dump(remain.items(), open("strongerin.json", "w"), default=lambda obj: (obj.isoformat() if isinstance(obj,
#                                                                                                       datetime.datetime) else None))

# fig,axs = plt.subplots(nrows=2)
# axs[0].plot(x_categories, brexit.values())
# axs[1].plot(x_categories, remain.values())
# axs[1].plot(x_categories, leave.values())
ax.xaxis.set_major_formatter(xfmt)
plt.legend()
# mpld3.show()
plt.show()