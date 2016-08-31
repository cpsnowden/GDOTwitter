import matplotlib.pyplot as plt
import numpy as np
import pycountry
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]
for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)


import random
data = [{"count":1770353,"_id":"Retweets"},{"count":3421286,"_id":"Original"}]
# random.shuffle(data)


# for j in data:
#     try:
#         j["_id"] = pycountry.languages.get(iso639_1_code=j["_id"]).name.partition(' ')[0]
#     except KeyError:
#         continue
# # exit()
print len(data)
# data.reverse()

total = sum([i["count"] for i in data]) + 0.0

labels = [i["_id"] + ": " + "{0:.1f}".format(100*i["count"]/total
                                             ) + "%" for i in data]
values = [i["count"] for i in data]



fig = plt.figure()
ax = plt.subplot()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()


fontsize = 14

_,texts = ax.pie(values, labels = labels, colors=[tableau20[0],tableau20[5]], labeldistance=1.05)
for i in texts:
    i.set_fontsize(fontsize)
# plt.yticks(y_values, labels, fontsize = fontsize)
# ax.tick_params(axis='x', labelsize=fontsize)
# plt.xlabel("Number of Times Retweeted", fontsize = fontsize)
# plt.yticks(np.arange(0, 1.1, 0.2), [str(x) for x in range(0, 101, 20)], fontsize=14)
plt.tight_layout()
plt.show()