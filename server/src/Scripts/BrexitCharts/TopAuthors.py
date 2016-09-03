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

#GNIP

data = [{"count":81389,"_id":"iVoteLeave"},{"count":57870,"_id":"iVoteStay"},{"count":29355,"_id":"Fight4UK"},{"count":22200,"_id":"Col_Connaughton"},{"count":21555,"_id":"RoyalNavyNews"},{"count":21049,"_id":"MikkiL"},{"count":20991,"_id":"brexitmarch"},{"count":15810,"_id":"SaraPadmore"},{"count":15260,"_id":"JodieActy"},{"count":14339,"_id":"mwengway"},{"count":14102,"_id":"marie52d"},{"count":13454,"_id":"Brndstr"},{"count":13438,"_id":"ukleave_eu"},{"count":11896,"_id":"EUVoteLeave23rd"},{"count":10640,"_id":"Vote4HEROES"},{"count":10064,"_id":"2053pam"},{"count":9976,"_id":"LewtonSerena5"},{"count":9934,"_id":"Margare39153871"},{"count":9930,"_id":"UKIPNFKN"},{"count":9775,"_id":"SimonPhillipsUK"}]

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


fontsize = 14

ax.barh(y_values, values, align='center', height = 0.7, color = tableau20[0], alpha = 0.7)
plt.yticks(y_values, labels, fontsize = fontsize)
plt.xticks(xrange(0,100000,20000), [str(i) for i in xrange(0,100,20)])
ax.tick_params(axis='x', labelsize=fontsize)
plt.xlabel("Number of Posts / thousand", fontsize = fontsize)
# plt.yticks(np.arange(0, 1.1, 0.2), [str(x) for x in range(0, 101, 20)], fontsize=14)
plt.tight_layout()
plt.show()