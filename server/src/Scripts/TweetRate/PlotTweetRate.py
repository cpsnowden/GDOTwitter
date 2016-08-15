import json

import matplotlib.dates as md
import matplotlib.pyplot as plt
import numpy as np
from dateutil import parser

import Scripts.TweetRate.ChangePoint

tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]
for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)

#######################################################################################################################
# path = "/Users/ChrisSnowden/Dropbox/1_Imperial College/Individual Project/FinalReport/Data/Brexit_Large_TweetRate.json"
# path =  "/Users/ChrisSnowden/IndividualProject/GDOTwitter/DATA/hourlyBrexit.dat"
# raw_data = []
# with open(path) as f:
#     for l in f:
#         raw_data.append(json.loads(l))


path =  "/Users/ChrisSnowden/IndividualProject/GDOTwitter/DATA/RAW_A_TwitterBre_7d.json"
with open(path) as f:
    data = json.load(f)
data = data["data"]
for i,series in enumerate(data["values"]):
    # print series
    if series["_id"] != "brexit":
        continue

    time = [parser.parse(i["dt"]) for i in series["data"]]
    counts = np.array([i["count"] for i in series["data"]]).astype(float) / 10e3


fig, axs = plt.subplots(nrows=2, sharex=True)
ax1 = axs[0]
# ax1 =axs
xfmt = md.DateFormatter('%Y-%m-%d\n %H:%M:%S')

ax1.xaxis.set_major_formatter(xfmt)
ax1.plot(time,counts)
ax1.set_ylabel("Tweets per day /10e3")

t = time[:len(time)/2]
c = counts[:len(time)/2]
y, zz, mean1, mean2 = Scripts.TweetRate.ChangePoint.step4(c)
print len(t),len(y)



ax2 = axs[1]
ax2.plot(t[1:],y)
ax2.set_ylabel("logP")
ax2.set_xlabel("Date")
plt.show()

#19th February "https://www.theguardian.com/world/live/2016/feb/19/eu-summit-all-night-negotiations-deal-cameron-live
# ?page=with:block-56c7aa56e4b041c56e71d202#block-56c7aa56e4b041c56e71d202"