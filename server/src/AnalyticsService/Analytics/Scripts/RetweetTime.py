from pymongo import MongoClient

from datetime import timedelta

db_col = MongoClient().get_database("DATA").get_collection("Brexit_old")


query = [
    {"$match":{"retweetedStatus":{"$exists":True}}},
    {"$group":{"_id":{"id":"$retweetedStatus.id","date":"$retweetedStatus.createdAt",
                      "name":"$retweetedStatus.user.screenName"},
               "retweets":{"$push":"$createdAt"}}}
]
# {"$match":{"retweets.length":{"$gte":2}}}


cursor = db_col.aggregate(query, allowDiskUse = True)
l = {}

#
for i,c in enumerate(cursor):
    retweets = c["retweets"]
    if len(retweets) < 10:
        continue
    ll = []
    bb = {}
    l[c["_id"]["id"]] = bb
    original_date = c["_id"]["date"]
    for d in retweets:
        dif = d - original_date
        # ll.append(dif)
        dif_seconds =(divmod(dif.seconds, 60)[0])
        if(dif_seconds not in bb):
            bb[dif_seconds] = 1
        else:
            bb[dif_seconds] +=1
    print i,bb


import pprint
pprint.pprint(l)

import json
json.dump(l,open("out2.dat","w"))
# "name":"$retweetedStatus.user.screenName"

