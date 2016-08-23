from dateutil import parser
from collections import OrderedDict
import matplotlib.pyplot as plt
import json
# import mpld3
# import matplotlib.dates as md
# dpi = 1
import numpy as np

tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]
for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)

path = "gnip_top_users.json"

with open(path) as f:
    data = json.load(f)

# i["_id"]["user-id"]

tweet_counts = np.array([i["count"] for i in data])
# print len(tweet_counts)
# print sum(tweet_counts)
# plt.plot(tweet_counts[:100000])


# plt.subplots(211)

ax = plt.subplot(111)
percentages = np.arange(101)
x = np.linspace(0,100,len(tweet_counts))
y =np.cumsum(tweet_counts).astype(float) / sum(tweet_counts)
resample = np.interp(percentages,x,y)
plt.plot(percentages,resample, lw = 1.5, color = tableau20[0])

plt.xlabel("Top x% of Users")
plt.ylabel("Account for y% of all Tweets")
plt.yticks(np.arange(0, 1.1, 0.2), [str(x) for x in range(0, 101, 20)], fontsize=14)
ax.spines["top"].set_visible(False)
# ax.spines["bottom"].set_visible(False)
ax.spines["right"].set_visible(False)
# ax.spines["left"].set_visible(False)
for y in np.arange(0,1.1,0.2):
    plt.plot(range(0,100),[y] * len(range(0,100)),"--", lw=0.5, color = "black", alpha = 0.3)
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
# plt.tick_params(axis="both", which="both", bottom="on", top="off", labelbottom="on", left="off", right="off",
#                 labelleft="on")
plt.text(-4,-0.1,"GNIP Brexit data set \nTotal number of users: 4,876,021 \nTotal number of tweets: 33,701,270",
         fontsize=10)
plt.plot([0, 1.85537, 1.85537],[0.5, 0.5, 0], color = tableau20[6], alpha = 0.3)
plt.text(2,0.25,"1.85% of users account for half of Brexit \ntweets from 1st Jan - 30th Jun",
         fontsize=10)
#

# plt.subplot(212)
# plt.hist(tweet_counts, bins="auto")


plt.show()