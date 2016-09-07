

import matplotlib.pyplot as plt
import numpy as np

tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]
for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)


data = [{"count":4269812,"_id":"brexit"},{"count":330630,"_id":"euref"},{"count":299588,"_id":"voteleave"},{"count":194854,"_id":"voteremain"},{"count":98942,"_id":"eurefresults"},{"count":87954,"_id":"eu"},{"count":83503,"_id":"leave"},{"count":80872,"_id":"remain"},{"count":72212,"_id":"ivoted"},{"count":65753,"_id":"strongerin"}]

data.reverse()

labels = [i["_id"] for i in data[-10:]]
values = [i["count"] for i in data[-10:]]
y_values = np.arange(len(labels)) + 0.5


fig = plt.figure()
ax = plt.subplot()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
import numpy as np

fontsize = 14

ax.barh(y_values, values, align='center', height = 0.7, color = tableau20[0], alpha = 0.7)
plt.yticks(y_values, labels, fontsize = fontsize)
plt.xticks(xrange(0,4500000,500000), [str(i) for i in np.arange(0,4.5,0.5)])
ax.tick_params(axis='x', labelsize=fontsize)
plt.xlabel("Number of usages / 10e5", fontsize = fontsize)
# plt.yticks(np.arange(0, 1.1, 0.2), [str(x) for x in range(0, 101, 20)], fontsize=14)
plt.tight_layout()
plt.show()