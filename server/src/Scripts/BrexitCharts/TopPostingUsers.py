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

data = [{"count": 3778, "_id": "iVoteStay"},
        {"count": 2737, "_id": "iVoteLeave"},
        {"count": 1650,"_id": "brexitmarch"},
        {"count": 1245, "_id": "Leavethe_EU"},
        {"count": 927, "_id": "Col_Connaughton"},
        {"count": 907, "_id": "RoyalNavyNews"},
        {"count": 873, "_id": "Fight4UK"},
        {"count": 743, "_id": "rotenyahu"},
        {"count": 708, "_id": "shaunmcg37"},
        {"count": 686, "_id": "UpNorthandGRIM"}]

data.reverse()

labels = [i["_id"] for i in data]
values = [i["count"] for i in data]
y_values = np.arange(len(labels)) + 0.5


fig = plt.figure()
ax = plt.subplot()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()


fontsize = 14

ax.barh(y_values, values, align='center', height = 0.7, color = tableau20[0], alpha = 0.7)
plt.yticks(y_values, labels, fontsize = fontsize)
ax.tick_params(axis='x', labelsize=fontsize)
plt.xlabel("Number of Tweets", fontsize = fontsize)
# plt.yticks(np.arange(0, 1.1, 0.2), [str(x) for x in range(0, 101, 20)], fontsize=14)
plt.tight_layout()
plt.show()