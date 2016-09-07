import json

import matplotlib.dates as md
import matplotlib.pyplot as plt
from dateutil import parser
from collections import OrderedDict
import numpy as np
import datetime
import random
name = "out.dat"
# These are the "Tableau 20" colors as RGB.
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]
# random.shuffle(tableau20)
# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.
for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)

def step4(d):

    n = len(d)
    dbar = np.mean(d)
    dsbar = np.mean(np.multiply(d,d))
    fac = dsbar - np.square(dbar)
    summ = 0
    summup = []

    for z in range(n):
        summ += d[z]
        summup.append(summ)
    y = []
    for m in range(n-1):
        pos = m+1
        mscale = 4 * pos * (n - pos)
        Q = summup[m] - (summ - summup[m])
        U = -np.square(dbar * (n-2*pos) + Q) / float(mscale) + fac
        y.append(-(n/float(2) - 1)*np.log(n * U/2) - 0.5*np.log(pos * (n-pos)))

    z,zz = np.max(y), np.argmax(y)

    mean1 = sum(d[:zz+1])/float(len(d[:zz+1]))
    mean2 = sum(d[(zz+1):n])/float(n-1-zz)

    return y, zz, mean1, mean2



def plot_time(name):
    with open(name) as f:
        data_root = json.loads(f.read(), object_pairs_hook=OrderedDict)
    n = 11
    cmap = plt.get_cmap('jet')
    colors = cmap(np.linspace(0, 1.0, n))
    data_root = OrderedDict(sorted(data_root.items(), key=lambda x: sum(x[1].values()), reverse=True))
    plt.figure(figsize=(12, 14))
    ax1 = plt.subplot(211)
    ax2 = plt.subplot(212, sharex = ax1)
    xfmt = md.DateFormatter('%Y-%m-%d\n %H:%M:%S')
    ax1.xaxis.set_major_formatter(xfmt)
    ax2.xaxis.set_major_formatter(xfmt)
    all = None
    for j,k in enumerate(data_root.keys()[:n]):

        print k

        data = data_root[k]
        counts = dict([(parser.parse(i),data[i]) for i in data.keys()])
        counts_sorted = [(i, counts[i]) for i in sorted(counts)]

        # if k == "all":
        #     nparray = np.array([i[1] for i in counts_sorted])
        #     np.savetxt("all.dat", nparray)

        # print counts_sorted
        # print counts_sorted
        time = [i[0] for i in counts_sorted]
        d = np.array([i[1] for i in counts_sorted])
        if k == "all":
            all = d,time
        ax1.plot(time,d, color = tableau20[j])
        if k not in ["all", "brexit"]:
            ax2.plot(time, d, color=tableau20[j])
        # y, zz, mean1, mean2 = step4([i[1] for i in counts_sorted])
        # print len(y), len(time)
        # ax2.plot(time[:-1], y, color = colors[j])
    ax1.spines["top"].set_visible(False)
    ax1.spines["bottom"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.spines["left"].set_visible(False)
    ax2.spines["top"].set_visible(False)
    ax2.spines["bottom"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    ax2.spines["left"].set_visible(False)
    for y in range(0, 3500, 500):
        ax1.plot(all[1], [y] * len(all[1]), "--", lw=0.5, color="black", alpha=0.3)
    for y in range(0, 1100, 100):
        ax2.plot(all[1], [y] * len(all[1]), "--", lw=0.5, color="black", alpha=0.3)
    ax1.legend(data_root.keys()[:n], bbox_to_anchor=(0., -.15, 1., .102), loc=2,
               ncol=6, mode="expand", borderaxespad=0., frameon=False)
    # ax1.legend(data_root.keys()[:n])
    plt.setp(ax1.get_xticklabels(), visible=False)
    # ax1.grid(True)
    # ax2.grid(True)
    ax1.get_xaxis().tick_bottom()
    ax1.get_yaxis().tick_left()
    ax2.get_xaxis().tick_bottom()
    ax2.get_yaxis().tick_left()
    plt.xlabel("Date (UTC)",fontsize = 15)
    ax1.set_ylabel("Tweets per minute", fontsize = 15)
    ax2.set_ylabel("Tweets per minute", fontsize = 15)
    dt = datetime.datetime(2016, 06, 24, 03, 50, 0)
    dt2 = datetime.datetime(2016, 06, 24, 04, 00, 0)
    # ax2.arrow(dt, 990, 0, -110, fc='k', ec='k')
    ax2.annotate("", xy=(dt, 890), xytext=(dt, 990),
                arrowprops=dict(arrowstyle="->"))
    ax2.text(dt2
             , 910, "Election Result Called by Media \n inc. BBC and ITV trigger spike \n in #EURef and #Leave",
             fontsize=14,
             color="b")
#
plot_time(name=name)
plt.show()

# # y,zz,mean1,mean2 = step4(d)
# # ax1 = plt.subplot(311)
# # ax1.plot(d)
# # ax1.plot([0,zz,zz,len(y)],[mean1,mean1,mean2,mean2])
# # ax2 = plt.subplot(312)
# # ax2.plot(y)
# # plt.show()
