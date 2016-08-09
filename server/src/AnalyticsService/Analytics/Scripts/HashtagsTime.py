import pandas as pd
from pymongo import MongoClient

from AnalysisEngine.TwitterObj import Status

time_quantum = "min"
db_col = MongoClient().get_database("DATA").get_collection("Brexit_old")


schema_id = "T4J"

limit = 30
mention_key = Status.SCHEMA_MAP[schema_id]["hashtags"]

top_user_query = [
    {"$unwind": "$" + mention_key},
    {"$group": {"_id": '$' + mention_key + '.' + 'text', "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": limit}]
# top_hastags = db_col.aggregate(top_user_query, allowDiskUse=True)
# a = list(top_hastags)

# print a
cursor = db_col.find({}, {Status.SCHEMA_MAP[schema_id]["created_at"]: 1, Status.SCHEMA_MAP[schema_id]["hashtags"]:
    1})

    # .limit(100)


a = [{u'count': 3605899, u'_id': u'Brexit'}, {u'count': 559956, u'_id': u'brexit'}, {u'count': 264322,
                                                                                             u'_id': u'VoteLeave'}, {u'count': 231881, u'_id': u'EUref'}, {u'count': 177952, u'_id': u'VoteRemain'}, {u'count': 95685, u'_id': u'EURefResults'}, {u'count': 92420, u'_id': u'BREXIT'}, {u'count': 79538, u'_id': u'EU'}, {u'count': 70626, u'_id': u'Leave'}, {u'count': 62210, u'_id': u'EURef'}, {u'count': 59497, u'_id': u'Remain'}, {u'count': 55568, u'_id': u'StrongerIn'}, {u'count': 50264, u'_id': u'BrexitVote'}, {u'count': 43090, u'_id': u'EUreferendum'}, {u'count': 43061, u'_id': u'UK'}, {u'count': 41897, u'_id': u'iVoted'}, {u'count': 41012, u'_id': u'BrexitOrNot'}, {u'count': 37329, u'_id': u'Bremain'}, {u'count': 27802, u'_id': u'LeaveEU'}, {u'count': 26985, u'_id': u'IndependenceDay'}, {u'count': 26220, u'_id': u'voteleave'}, {u'count': 25175, u'_id': u'Trump'}, {u'count': 24637, u'_id': u'ivoted'}, {u'count': 23600, u'_id': u'referendum'}, {u'count': 21058, u'_id': u'euref'}, {u'count': 19749, u'_id': u'UE'}, {u'count': 19577, u'_id': u'Trump2016'}, {u'count': 19175, u'_id': u'remain'}, {u'count': 17338, u'_id': u'IVotedLeave'}, {u'count': 15541, u'_id': u'Britain'}]

# hashtags = ["voteleave","brexit","voteremain"]
hashtags = set([i['_id'].lower() for i in a] + ["all"])
dates = []
used =  dict([(i,[]) for i in hashtags])
print used
# print used
for c in cursor:
    s = Status(c, schema_id)
    dates.append(s.get_created_at())
    htags = [h.lower() for h in s.get_hashtags()]
    for h in hashtags:
        if h == "all":
            continue
        if h in htags:
            used[h].append(1)
        else:
            used[h].append(0)
    used["all"].append(1)
# print used
index = pd.DatetimeIndex(dates)
#
#
#
#
#
# dates = [Status(c, schema_id).get_created_at()
#          for c in db_col.find({}, {Status.SCHEMA_MAP[schema_id]["created_at"]: 1}).limit(100)]

df = pd.DataFrame(used, index=index, columns=hashtags)

gb = df.groupby(pd.TimeGrouper(freq=time_quantum)).sum()

data = gb.to_json(date_format='iso')
with open("out.dat","w") as f:
    f.write(data)

print
import pprint
pprint.pprint(gb.to_dict())