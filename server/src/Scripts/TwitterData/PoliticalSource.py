import matplotlib.pyplot as plt

data = [(68, 73, 68, 68, 60),
        (20, 15, 15, 15, 12),
        (0, 1, 4, 6, 15),
        (8, 8, 8, 7, 8),
        (2, 1, 2, 1, 2),
        (1, 1, 2, 1, 1),
        (1, 1, 1, 2, 2)]

data = [
    ("Television", (78, 75, 86, 78, 72)),
    ("Magazines", (4, 4, 3, 2, 4)),
    ("Internet", (0, 2, 7, 13, 26)),
    ("Other", (3, 1, 3, 2, 3)),
    ("Radio", (17, 18, 14, 15, 13)),
    ("Unknown", (1, 1, 1, 2, 2)),
    ("Newspaper", (47, 49, 36, 38, 30))
]
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]
for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)

# data = sorted(data, key=lambda x:x[0], reverse=True)

import numpy as np

ndata = np.array([i[1] for i in data]).astype(float)
print np.sum(ndata, axis=0)
ndata = 100 * ndata / np.sum(ndata, axis=0)
print ndata
labels = ["Feb 1992", "Feb 1996", " Jan 2000", "Jan 2004", "Late Dec 2007"]

y_stack = np.cumsum(ndata, axis=0)
print y_stack
f, ax = plt.subplots()

x = np.arange(len(labels))
color = [0, 7, 1, 2, 5, 18, 6]
r1 = ax.fill_between(x, 0, y_stack[0, :], color=tableau20[0])
r2 = ax.fill_between(x, y_stack[0, :], y_stack[1, :], color=tableau20[7], alpha=0.4)
r3 = ax.fill_between(x, y_stack[1, :], y_stack[2, :], color=tableau20[1], alpha=0.4)
r4 = ax.fill_between(x, y_stack[2, :], y_stack[3, :], color=tableau20[2], alpha=0.4)
r5 = ax.fill_between(x, y_stack[3, :], y_stack[4, :], color=tableau20[5], alpha=0.4)
r6 = ax.fill_between(x, y_stack[4, :], y_stack[5, :], color=tableau20[18], alpha=0.4)
r7 = ax.fill_between(x, y_stack[5, :], y_stack[6, :], color=tableau20[6], alpha=0.4)

# plt.legend([r1, r2, r3, r4, r5, r6, r7],
#            [i[0] for i in data],
#            loc="lower center", ncol=7, bbox_to_anchor=(0.5, -0.12), fontsize=10)

# plt.xlabel("Year")
plt.ylabel("Percentage of surveyed American adults listing \n category in top two sources for political content",
           fontsize=14)

plt.yticks(np.arange(0, 110, 20), [str(x) for x in range(0, 110, 20)], fontsize=14)
plt.ylim([0, 100])
plt.xlim([0, 4])
plt.xticks(xrange(len(labels)), labels,fontsize=14)

y_levels = [0] + [i[-1] for i in y_stack]
print y_levels
for i in xrange(len(data)):
    ax.text(4.02, (y_levels[i] + y_levels[i+1])/2.0, data[i][0], color=tableau20[color[i]], fontsize=14)

# ax.annotate("Blah", (4.1,25),(4.3,25), arrowprops=dict(arrowstyle="-[,widthB=10",connectionstyle="arc3,rad=-0.05"))

# ax.set_xticks(np.array(x) + 0.4)
# ax.set_xticklabels([i[0] for i in data])
# ax.spines["top"].set_visible(False)
# ax.spines["right"].set_visible(False)
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()

plt.show()
