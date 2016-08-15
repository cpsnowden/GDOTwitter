import pandas as pd
import matplotlib.pyplot as plt
import json
from dateutil import parser
from collections import OrderedDict
import numpy as np


brexit = json.load(open("brexit.json"))
leave = json.load(open("leave.json"))
remain = json.load(open("remain.json"))
f, ax = plt.subplots(2, 1, sharex=True)

def plot_changes(data, l):
    df = pd.DataFrame.from_dict(OrderedDict([(parser.parse(i),j) for i,j in data]), orient="index")
    df.columns = ["count"]
    ma = pd.ewma(df,15)
    stdev = ma.std()
    # stdev = pd.rolling_std(df, 24)

    print df

    find_events(df, ma, stdev, l )

def find_events(df, ma,  stdev, l, alpha = 0.25):
    df["limit"]  = ma + alpha * stdev
    df["event"] = df["count"] > df["limit"]
    df["block"] = (df["event"].shift(1) != df["event"]).astype(int).cumsum()

    ax[0].plot(df.index, df["count"])
    ax[0].plot(df.index, ma)
    ax[0].plot(df.index, df["limit"])
    #
    # ax[1].plot(df.index, df["event"])
    # ax[1].plot(df.index, df["block"])
    event_flags =  df.reset_index().groupby(['event', 'block'])['index'].apply(lambda x: np.array(x))

    k =  event_flags.ix[True]
    ev = []
    for K in k:
        ev.append((K[0],K[-1]))
    for s,e in ev:
        plt.axvspan(s,e, l[0] / l[1], (l[0] + 1)/l[1])

# plot_changes(brexit)
import matplotlib.dates as md
xfmt = md.DateFormatter('%Y-%m-%d\n %H:%M:%S')
ax[0].xaxis.set_major_formatter(xfmt)
ax[1].xaxis.set_major_formatter(xfmt)
from statsmodels.tsa.seasonal import seasonal_decompose

# df = pd.DataFrame.from_dict(OrderedDict([(parser.parse(i),j) for i,j in brexit]), orient="index")
# df.columns = ["count"]
#
# df.reset_index(inplace=True)
# df['Date'] = pd.to_datetime(df.index)
# df = df.set_index('Date')
#
# print df
# decomposition = seasonal_decompose(df['count'], model='additive')
# fig = plt.figure()
# fig = decomposition.plot()

plot_changes(brexit, (0.0,3.0))
plot_changes(leave, (1.0,3.0))
plot_changes(remain,(2.0,3.0))
# #
# # df = pd.DataFrame.from_dict(OrderedDict([(parser.parse(i),j) for i,j in brexit]), orient="index")
# # df.columns = ["count"]
# # ax[0].plot(df.index,df["count"])
# # ax[1].plot(df.index, df["count"] - df["count"].shift())
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