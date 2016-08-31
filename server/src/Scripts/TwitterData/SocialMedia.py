import matplotlib.pyplot as plt


data = [(2005, 12, 8, 5, 2),
        (2006, 41, 6, 3, 0),
        (2008, 63, 27, 9, 2),
        (2009, 72, 44, 22, 7),
        (2010, 78, 53, 33, 11),
        (2011, 80, 60, 37, 13),
        (2012, 83, 67, 43, 19),
        (2013, 88, 73, 52, 26),
        (2014, 84, 77, 52, 27),
        (2015, 90, 77, 51, 35)]

labels = ["18-29", "30-49", "50-64", "65+"]

tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]
for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)

import numpy as np


fig, ax = plt.subplots()

x_values = [0,1,3,4,5,6,7,8,9,10]

for j in xrange(1,5):
        ax.plot(x_values, [i[j] for i in data], lw = 2, alpha = 0.7, color = tableau20[j*2], label = labels[j-1])

# ax.set_ylabel('Monthly Active Users /million')


plt.yticks(np.arange(0, 110, 20), [str(x) for x in range(0, 110, 20)], fontsize=14)
plt.xticks(xrange(0,11), xrange(2005,2016))
# ax.set_xticks(np.array(x) + 0.4)
# ax.set_xticklabels([i[0] for i in data])
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
plt.legend(loc="lower center", ncol=4, bbox_to_anchor=(0.5,-0.12), fontsize=10)
# plt.xlim([0, max(x)+ 1.2])
#
for y in range(20, 110, 20):
    ax.plot([0, max(x_values)], [y]*2, "--", lw=0.5, color="black", alpha=0.3)
#
plt.xlabel("Year")
plt.ylabel("Percentage of Americans using Social Networking Sites")

plt.show()
