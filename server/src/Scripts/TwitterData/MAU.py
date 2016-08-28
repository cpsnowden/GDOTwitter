import matplotlib.pyplot as plt

tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]
for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)

data = [
("Q1\n'10",	30),
("Q2\n'10",	40),
("Q3\n'10",	49),
("Q4\n'10",	54),
("Q1\n'11",	68),
("Q2\n'11",	85),
("Q3\n'11",	101),
("Q4\n'11",	117),
("Q1\n'12",	138),
("Q2\n'12",	151),
("Q3\n'12",	167),
("Q4\n'12",	185),
("Q1\n'13",	204),
("Q2\n'13",	218),
("Q3\n'13",	231.7),
("Q4\n'13",	241),
("Q1\n'14",	255),
("Q2\n'14",	271),
("Q3\n'14",	284),
("Q4\n'14",	288),
("Q1\n'15",	302),
("Q2\n'15",	304),
("Q3\n'15",	307),
("Q4\n'15",	305),
("Q1\n'16",	310),
("Q2\n'16",	313)]
import numpy as np

values = [i[1] for i in data]
x = np.arange(len(values))

fig, ax = plt.subplots()

rects2 = ax.bar(x + 0.2, values, 0.8, color=tableau20[0], alpha=0.4)

ax.set_ylabel('Monthly Active Users /million')
ax.set_xticks(np.array(x) + 0.4)
ax.set_xticklabels([i[0] for i in data])
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
plt.xlim([0, max(x)+ 1.2])

for y in range(0, 400, 50):
    ax.plot([0, max(x)+1.2], [y]*2, "--", lw=0.5, color="black", alpha=0.3)

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.0*height,
                '%d' % int(height),
                ha='center', va='bottom')


autolabel(rects2)

plt.show()
