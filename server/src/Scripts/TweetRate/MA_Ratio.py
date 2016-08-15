import json
from collections import OrderedDict
from statsmodels.tsa.stattools import acf, pacf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dateutil import parser
from statsmodels.tsa.arima_model import ARIMA

brexit = OrderedDict(json.load(open("brexit.json")))
leave = OrderedDict(json.load(open("leave.json")))
remain = OrderedDict(json.load(open("strongerin.json")))
N = 3.0
f, ax = plt.subplots(4, 1, sharex=True)
i = 0.0

def plot_tweet_rate(ax1, ax2, ax3, ax4, brexit, leave, remain):
    df = pd.DataFrame.from_dict(OrderedDict([(parser.parse(i),
                                              {"brexit": j,
                                               "leave": leave[i],
                                               "remain": remain[i]}) for i, j in brexit.items()]), orient="index")

    ax1.plot(df.index, df["brexit"])
    find_events(df["brexit"], ax1, ax4)
    ax1.set_title("Brexit")
    ax2.plot(df.index, df["leave"])
    find_events(df["leave"], ax2, ax4)
    ax2.set_title("VoteLeave")
    ax3.plot(df.index, df["remain"])
    find_events(df["remain"], ax3, ax4)
    ax3.set_title("StrongerIn")



def find_events(series, ax, ax_event, alpha=1.2):
    global i, N
    ma = pd.rolling_mean(series, 24)
    # stdev = pd.ewmstd(series,20)
    stdev = series.std()
    ax.plot(ma.index, ma)
    threshold =  series.mean() + pd.rolling_std(series, 24)
    df = series.to_frame(name = "count")
    df["limit"] = ma + alpha * stdev
    df["event"] = (df["count"] > df["limit"]) & (df["count"] > (threshold))
    df["mult"] = ma / df["limit"]
    df["block"] = (df["event"].shift(1) != df["event"]).astype(int).cumsum()
    ax.plot(df.index, threshold)
    ax.plot(df.index, df["limit"])

    event_flags = df.reset_index().groupby(['event', 'block'])['index'].apply(lambda x: np.array(x))
    k = event_flags.ix[True]
    ev = []
    for K in k:
        ev.append((K[0], K[-1]))
    for s, e in ev:
        ax_event.axvspan(s, e, i/N, (i + 1) / N)
    i += 1

# plot_changes(brexit)
import matplotlib.dates as md

xfmt = md.DateFormatter('%Y-%m-%d\n %H:%M:%S')
ax[0].xaxis.set_major_formatter(xfmt)
ax[1].xaxis.set_major_formatter(xfmt)

plot_tweet_rate(ax[0], ax[1],ax[2], ax[3], brexit, leave, remain)

# plot_changes(leave_ratios, (0.0,2.0))
# plot_changes(remain_ratios, (1.0,2.0))
# plot_changes(remain,(2.0,3.0))
plt.show()




# series = twitter_example_data["count"]
# print series
# twitter_ma = pd.rolling_mean(series, 24)
#
# twitter_example_data['timestamp'] = pd.to_datetime(twitter_example_data['timestamp'])
# twitter_example_data.set_index('timestamp', drop=True)
# # stdev = pd.rolling_std(twitter_ma,24)
# stdev = twitter_ma.std()
# print stdev
# # plt.subplot(211)
# plt.plot(twitter_example_data['timestamp'], twitter_ma, 'r')
# plt.plot(twitter_example_data['timestamp'], twitter_ma + 0.25 * stdev, 'k')
# plt.plot(twitter_example_data['timestamp'], twitter_example_data['count'], 'b')
# # plt.subplot(212)
# # plt.plot(twitter_example_data['timestamp'], stdev, 'k')
#
# plt.show()
#



# n = twitter_example_data.shape[0]
# print n
#
#
# def get_anomolies(data):
#     return detect_ts(data, max_anoms=0.01, alpha=0.01, direction='pos', only_last=None)
#
# steps = xrange(0, n, n/5)
# anoms = {"anoms":None}
# for i in xrange(len(steps)-1):
#     print steps[i],steps[i+1]
#
#     data_slice = twitter_example_data[steps[i]:steps[i+1]]
#     data_slice.reset_index(drop=True, inplace=True)
#     # print data_slice
#     r= get_anomolies(deepcopy(data_slice))
#     if i == 0:
#         anoms["anoms"] = r["anoms"]
#     else:
#         anoms["anoms"] =  anoms["anoms"].append(r["anoms"])
#
#
# # twitter_example_data = pd.read_csv('brexit.csv', usecols=['timestamp', 'count'])
# # twitter_example_data = twitter_example_data[:1000]
# # format the twitter data nicely
# twitter_example_data['timestamp'] = pd.to_datetime(twitter_example_data['timestamp'])
# twitter_example_data.set_index('timestamp', drop=True)
# #
# # # make a nice plot
# f, ax = plt.subplots(2, 1, sharex=True)
# ax[0].plot(twitter_example_data['timestamp'], twitter_example_data['count'], 'b')
# ax[0].plot(anoms['anoms'].index, anoms    ['anoms']['anoms'], 'ro')
# ax[0].set_title('Detected Anomalies')
# ax[1].set_xlabel('Time Stamp')
# ax[0].set_ylabel('Count')
# ax[1].plot(anoms['anoms'].index, anoms['anoms']['anoms'], 'b')
# ax[1].set_ylabel('Anomaly Magnitude')
# plt.show()
