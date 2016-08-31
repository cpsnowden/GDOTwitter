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
data = [{"count":3452921,"_id":"en"},{"count":481494,"_id":"es"},{"count":343469,"_id":"fr"},{"count":251220,
                                                                                              "_id":"Unknown"},
        {"count":192827,"_id":"it"},{"count":129743,"_id":"de"},{"count":56739,"_id":"nl"},{"count":43412,"_id":"el"},{"count":38607,"_id":"tr"},{"count":30597,"_id":"th"},{"count":23131,"_id":"pt"},{"count":20174,"_id":"pl"},{"count":18722,"_id":"ar"},{"count":14305,"_id":"ru"},{"count":14263,"_id":"sv"},{"count":13836,"_id":"in"},{"count":10397,"_id":"ja"},{"count":8470,"_id":"fi"},{"count":6308,"_id":"tl"},{"count":5721,"_id":"da"},{"count":5634,"_id":"hi"},{"count":4030,"_id":"cs"},{"count":3371,"_id":"no"},{"count":2708,"_id":"ht"},{"count":2344,"_id":"ro"},{"count":2006,"_id":"uk"},{"count":1907,"_id":"et"},{"count":1468,"_id":"cy"},{"count":1349,"_id":"fa"},{"count":1209,"_id":"ko"},{"count":1148,"_id":"lv"},{"count":1052,"_id":"eu"},{"count":811,"_id":"ur"},{"count":806,"_id":"sl"},{"count":766,"_id":"sr"},{"count":641,"_id":"lt"},{"count":582,"_id":"bg"},{"count":578,"_id":"hu"},{"count":529,"_id":"is"},{"count":472,"_id":"zh"},{"count":437,"_id":"ne"},{"count":366,"_id":"ta"},{"count":263,"_id":"mr"},{"count":224,"_id":"iw"},{"count":116,"_id":"gu"},{"count":113,"_id":"vi"},{"count":102,"_id":"ml"},{"count":86,"_id":"te"},{"count":61,"_id":"bn"},{"count":25,"_id":"kn"},{"count":22,"_id":"ka"},{"count":17,"_id":"am"},{"count":17,"_id":"hy"},{"count":17,"_id":"si"},{"count":2,"_id":"my"},{"count":2,"_id":"ckb"},{"count":1,"_id":"pa"},{"count":1,"_id":"ps"}]
data = data[:10] + [{"count":sum([i["count"] for i in data[10:]]),"_id":"other"}]
# random.shuffle(data)


for j in data:
    try:
        j["_id"] = pycountry.languages.get(iso639_1_code=j["_id"]).name.partition(' ')[0]
    except KeyError:
        continue
# exit()
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