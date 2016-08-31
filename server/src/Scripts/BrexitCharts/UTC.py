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
data = [{"count":1735905,"_id":"Unspecified"},{"count":791670,"_id":"UTC+2.0"},{"count":636497,"_id":"UTC+1.0"},{"count":501154,"_id":"UTC-7.0"},{"count":332078,"_id":"UTC-4.0"},{"count":307411,"_id":"UTC-5.0"},{"count":218030,"_id":"UTC+3.0"},{"count":114735,"_id":"UTC-3.0"},{"count":70049,"_id":"UTC"},{"count":63243,"_id":"UTC-2.0"},{"count":58371,"_id":"UTC+5.5"},{"count":54341,"_id":"UTC+8.0"},{"count":53188,"_id":"UTC-6.0"},{"count":52733,"_id":"UTC-10.0"},{"count":52190,"_id":"UTC+10.0"},{"count":33655,"_id":"UTC+7.0"},{"count":22167,"_id":"UTC+9.0"},{"count":18805,"_id":"UTC-4.5"},{"count":13517,"_id":"UTC-8.0"},{"count":12336,"_id":"UTC+5.0"},{"count":10806,"_id":"UTC-11.0"},{"count":10284,"_id":"UTC+4.0"},{"count":8630,"_id":"UTC+12.0"},{"count":5917,"_id":"UTC+4.5"},{"count":4661,"_id":"UTC+6.0"},{"count":3805,"_id":"UTC+9.5"},{"count":1905,"_id":"UTC+11.0"},{"count":1234,"_id":"UTC+5.75"},{"count":1095,"_id":"UTC-2.5"},{"count":582,"_id":"UTC+13.0"},{"count":341,"_id":"UTC+6.5"},{"count":278,"_id":"UTC-1.0"},{"count":19,"_id":"UTC+10.5"},{"count":7,"_id":"UTC-9.0"}]
data = data[:15] + [{"count":sum([i["count"] for i in data[15:]]),"_id":"Other"}]
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

_,texts = ax.pie(values, labels = labels, colors=tableau20, labeldistance=1.05)
for i in texts:
    i.set_fontsize(fontsize)
# plt.yticks(y_values, labels, fontsize = fontsize)
# ax.tick_params(axis='x', labelsize=fontsize)
# plt.xlabel("Number of Times Retweeted", fontsize = fontsize)
# plt.yticks(np.arange(0, 1.1, 0.2), [str(x) for x in range(0, 101, 20)], fontsize=14)
plt.tight_layout()
plt.show()