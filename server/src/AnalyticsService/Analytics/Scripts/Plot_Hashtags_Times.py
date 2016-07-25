import json
import matplotlib.pyplot as plt
import numpy as np
from collections import OrderedDict
from scipy import interpolate
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


f = json.load(open("out2.dat","r"))
data_root = OrderedDict(sorted(f.items(), key=lambda x: sum(x[1].values()), reverse=True))
time = np.arange(2000)
data = np.zeros(len(time))
for i in data_root.keys():
    k = f[i]
    for i in k.keys():
        if(int(i) < 2000):
            data[int(i)] += k[i]
    # j = k.items()
    # # print j[:30]
    # sorted_k = sorted(j, key = lambda x:int(x[0]))
    # # print sorted_k[:30]
    # plt.plot([j[0] for j in sorted_k], [j[1] for j in sorted_k])
fig, ax1 = plt.subplots()

j = 0
k = 6
ax1.semilogx(time/60.0,data / sum(data), color = tableau20[j])
ax1.set_ylabel("Fraction of retweets occuring at one minute interval", color = tableau20[j])
for tl in ax1.get_yticklabels():
    tl.set_color(tableau20[j])
ax2 = ax1.twinx()
ax2.semilogx(time/60.0,np.cumsum(data) / sum(data), color = tableau20[k])
ax2.set_ylabel("Fraction of retweets occuring before t", color = tableau20[k])
for tl in ax2.get_yticklabels():
    tl.set_color(tableau20[k])
ax1.set_xlabel("Time (t) since original tweet was published /hours")
plt.xlim([0, 1400/60])

ax2.plot([1.3257, 1.3257, 1400],[0,0.5,0.5], color = tableau20[k], linestyle = "--")
ax2.text(1.3257
         ,0.51, "50% of retweets within 1.3hrs of the original",
         fontsize=14,
         color="b")
yToFind = 0.5
yreduced = np.array(np.cumsum(data) / sum(data)) - yToFind
freduced = interpolate.UnivariateSpline(time/60.0, yreduced, s=0)

print freduced.roots()
plt.show()
