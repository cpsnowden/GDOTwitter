import matplotlib.dates as md
import matplotlib.pyplot as plt
from dateutil import parser
from collections import OrderedDict
import numpy as np
import datetime
import json
import string
es = []
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]
for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)
def plot(path,ax):
    global k
    data = json.load(open(path))


    rates = OrderedDict([[parser.parse(i[0]),i[1]] for i in data["data"]])




    ax.plot(rates.keys(), rates.values(), color=tableau20[0])
    #
    # start_date = datetime.datetime(2016, 06, 23, 20)
    # end_date = datetime.datetime(2016, 06, 24, 10)

    events = data["event"]

    letters = list(string.ascii_uppercase) + [("A" + i) for i in string.ascii_uppercase] + [("B" + i) for i in
                                                                                            string.ascii_uppercase]
    j = 0
    for i,event in enumerate(events):
        if parser.parse(event["start"]) < start_date:
            continue
        print i
        c = divmod(j,len(anotation_height))[1]
        ax.axvspan(parser.parse(event["start"]), parser.parse(event["end"]), y_mins[c], y_max[c], color=tableau20[10],
                   alpha=0.2,
                   lw=0)
        ax.text(parser.parse(event["midpoint"]), anotation_height[c], letters[k],
                ha="center",
                size=10,
                bbox=dict(boxstyle="circle", fc="w", ec="k"))

        es.append({letters[k]:{"top_words":event["top_words"],"titles":event["guardian_titles"]}})
        j += 1
        k += 1


    ax.plot([rates.keys()[0],rates.keys()[-1]],[0,0], color = "k")
    ax.set_xlim([start_date, max(rates.keys())])

    # plt.xticks(dates, [i.strftime("%a %d %b \n%H:%M") for i in dates])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    ax.spines["bottom"].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

k = 0
fig, ax = plt.subplots(nrows=3)
ax[0].set_xticks([])
ax[2].set_xticks([])
ax[0].set_ylabel("#strongerin \n tweet rate 10e3/hour", fontsize=14)
ax[1].set_ylabel("#brexit \n tweet rate 10e3/hour", fontsize=14)
ax[2].set_ylabel("#voteleave \n tweet rate 10e3/hour", fontsize=14)

ax[0].set_ylim([-1000, 10000])
ax[1].set_ylim([0, 450000])
ax[2].set_ylim([-4000, 35000])
start_date = datetime.datetime(2016,5,01)
# ax[1].set_xticks([])
ax[0].plot([start_date,start_date],[0,9000], color = "k")
ax[1].plot([start_date,start_date],[0,400000], color = "k")
ax[2].plot([start_date,start_date],[0,30000], color = "k")
# ax[0].set_ylim([-1000, 10000])
ax[0].set_yticklabels(xrange(0, 10,1), fontsize = 14)
ax[1].set_yticklabels(xrange(0, 401,50), fontsize = 14)
ax[2].set_yticklabels(xrange(0, 36,5), fontsize = 14)
ax[0].set_yticks(xrange(0, 10000,1000))
ax[1].set_yticks(xrange(0, 401000,50000))
ax[2].set_yticks(xrange(0, 35000,5000))
anotation_height = [10200, 9300, -550, -1450]
anotation_height = [anotation_height[0], anotation_height[2], anotation_height[1], anotation_height[3]]
y_mins = [1000,1000, 500, 0]
y_mins = [y_mins[0], y_mins[2], y_mins[1], y_mins[3]]
y_max = [11000, 10500, 10000,10000]
y_max = [y_max[0], y_max[2], y_max[1], y_max[3]]
y_mins = [i/float(11000) for i in y_mins]
y_max =  [i/float(11000) for i in y_max]

plot("strongerin_events.json", ax[0])
xfmt = md.DateFormatter('%d %b')
ax[1].xaxis.set_major_formatter(xfmt)
anotation_height = [400000, 350000]

y_mins = [0,0]

y_max = [0.9,0.8]



plot("brexit_events.json", ax[1])

anotation_height = [35000, 33000, -2000, -4000]
anotation_height = [anotation_height[0], anotation_height[2], anotation_height[1], anotation_height[3]]
y_mins = [4000,4000, 2000, 0]
y_mins = [y_mins[0], y_mins[2], y_mins[1], y_mins[3]]
y_max = [35000 + 4000, 33000 + 4000, 30000 + 4000,30000 + 4000]
y_max = [y_max[0], y_max[2], y_max[1], y_max[3]]
y_mins = [i/float(39000) for i in y_mins]
y_max =  [i/float(39000) for i in y_max]
ax[1].tick_params(axis='x', labelsize=14)
plot("voteleave_events.json", ax[2])


json.dump(es, open("event_mapping.json","w"))

ax[1].set_xlabel("Date /UTC", fontsize = 16)

plt.show()
