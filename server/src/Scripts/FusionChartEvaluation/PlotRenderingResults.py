import json
from collections import OrderedDict
import matplotlib.pyplot as plt
import pprint
import numpy as np

tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]
for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)

raw = json.load(open("ResultsRendering.json"))

sorted_results = sorted(raw.items(), key=lambda x: x[1]["width"])
# pprint.pprint(sorted_results)
width, render_means = zip(*[(i[1]["width"],np.mean(i[1]["results"]["render"])) for i in sorted_results])
render_std = [np.std(i[1]["results"]["render"])  for i in sorted_results]

sqrt_len = [np.sqrt(len((i[1]["results"]["render"])))  for i in sorted_results]
print sqrt_len
stderr = [float(render_std[i])/sqrt_len[i] for i in xrange(len(sqrt_len))]

print stderr
# pprint.pprint(render_means)


ax = plt.subplot(111)
l1 = ax.errorbar(width, render_means, yerr=stderr, lw = 1.5, color = tableau20[0])
plt.xlabel("Width of Canvas /px")
plt.ylabel("Time to Render /s")
plt.yticks(np.arange(10000,21000,2000), [str(x/1000.0) for x in range(10000, 21000, 2000)], fontsize=14)
ax.spines["top"].set_visible(False)
# ax.spines["bottom"].set_visible(False)
ax.spines["right"].set_visible(False)
# ax.spines["left"].set_visible(False)
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()


z = np.polyfit(width, render_means, 1)
p = np.poly1d(z)
plt.plot(width,p(width),"r--")
# for y in np.arange(0,1.1,0.2):
#     plt.plot(range(0,100),[y] * len(range(0,100)),"--", lw=0.5, color = "black", alpha = 0.3)

for y in np.arange(10000,21000,2000):
    plt.plot(range(0,30000),[y] * len(range(0,30000)),"--", lw=0.5, color = "black", alpha = 0.3)

plt.show()