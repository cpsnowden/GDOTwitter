import datetime

import pandas as pd

dates =  [datetime.datetime(2011,01,01), datetime.datetime(2012,01,01)]
sentiment = {"neg":[0,1],"pos":[2,0]}

index = pd.DatetimeIndex(dates)

df = pd.DataFrame(sentiment, index=index)
gb = df.groupby(pd.TimeGrouper(freq="M")).sum()
gb.fillna(0.0, inplace=True)

# data_dict = gb.to_dict()
# values = dict([(key, []) for key in data_dict.keys()])
# for series_name, series_data in data_dict.iteritems():
#     values[series_name] += [{"dt": dt, "count": count} for (dt, count) in series_data.iteritems()]
#
# data = [{"_id": id, "data": data} for (id, data) in values.iteritems()]
# x_values = gb.index.tolist()


data_dict = gb.to_dict()
print data_dict
values = dict([(key, []) for key in data_dict.keys()])

data = [{"_id":series_name, "data":[{"dt": dt, "count": count} for (dt, count) in series_data.iteritems()]} for
        series_name, series_data in data_dict.iteritems()]

x_values = gb.index.tolist()

# d =  gb.to_dict()
# print d.keys()
# values = dict([(key,[]) for key in d.keys()])
# print values
#
# for series_name, series_data in d.iteritems():
#     # print series_name, series_data
#     for dt, count in series_data.iteritems():
#         values[series_name].append({"dt":dt, "count": count})

# v = []
# for id, data in values.iteritems():
#     v.append({"_id":id, "data":data})

print
import pprint

pprint.pprint(data)
# pprint.pprint(gb.index.tolist())
# pprint.pprint(values)
# pprint.pprint(v)
# print json.dumps(v, default=Util.date_encoder)