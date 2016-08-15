import pandas as pd
import matplotlib.pyplot as plt
from pyculiarity import detect_ts
from copy import deepcopy
# first run the models
twitter_example_data = pd.read_csv('brexit.csv', usecols=['timestamp', 'count'])

n = twitter_example_data.shape[0]
print n


def get_anomolies(data):
    return detect_ts(data, max_anoms=0.01, alpha=0.01, direction='pos', only_last=None, longterm=True)

steps = xrange(0, n, n/5)
anoms = {"anoms":None}
for i in xrange(len(steps)-1):
    print steps[i],steps[i+1]

    data_slice = twitter_example_data[steps[i]:steps[i+1]]
    data_slice.reset_index(drop=True, inplace=True)
    # print data_slice
    r= get_anomolies(deepcopy(data_slice))

    if i == 0:
        anoms["anoms"] = r["anoms"]
    else:
        anoms["anoms"] =  anoms["anoms"].append(r["anoms"])


# twitter_example_data = pd.read_csv('brexit.csv', usecols=['timestamp', 'count'])
# twitter_example_data = twitter_example_data[:1000]
# format the twitter data nicely
twitter_example_data['timestamp'] = pd.to_datetime(twitter_example_data['timestamp'])
twitter_example_data.set_index('timestamp', drop=True)
#
# # make a nice plot
f, ax = plt.subplots(2, 1, sharex=True)
ax[0].plot(twitter_example_data['timestamp'], twitter_example_data['count'], 'b')
ax[0].plot(anoms['anoms'].index, anoms['anoms']['anoms'], 'ro')
ax[0].set_title('Detected Anomalies')
ax[1].set_xlabel('Time Stamp')
ax[0].set_ylabel('Count')
ax[1].plot(anoms['anoms'].index, anoms['anoms']['anoms'], 'b')
ax[1].set_ylabel('Anomaly Magnitude')
plt.show()