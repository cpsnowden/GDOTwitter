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

plt.plot(tweet_counts[:100000])

# percentages = np.arange(101)
# x = np.linspace(0,100,len(tweet_counts))
# y =np.cumsum(tweet_counts).astype(float) / sum(tweet_counts)
#
# resample = np.interp(percentages,x,y)
#
# plt.plot(percentages,resample)
#
#


plt.show()