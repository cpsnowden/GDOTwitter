import datetime
import json
import pprint

from pymongo import MongoClient

from Scripts.DateGroupingUtils import get_date_projection

date_encoder = lambda obj: (obj.isoformat() + "Z" if isinstance(obj, datetime.datetime) else None)

db_col = MongoClient().get_database("DATA").get_collection("BrexitRemain_old")

date_field = "createdAt"
dolar_date_field = "$" + date_field

p1, p2 = get_date_projection(dolar_date_field, "Day")

uw = {"$unwind": "$hashtagEntities"}
m = {"$match": {"hashtag":"voteremain"}}

p1["hashtag"] = {"$toLower":"$hashtagEntities.text"}
p1 = {"$project": p1}
p2["hashtag"] = "$hashtag"
p2 = {"$project": p2}
g1 = {"$group": {"_id": {"dt": "$date", "hashtag": "$hashtag"}, "count": {"$sum": 1}}}
s1 = {"$sort": {"_id.dt": 1}}
p3 = {"$group":{"_id":"$_id.hashtag","data":{"$push":{"dt":"$_id.dt", "count":"$count"}}}}

query = [uw,p1,m,p2,g1,s1, p3]
# print query
c = db_col.aggregate(query, allowDiskUse=True)

result = {
    "details": {"chartType": "line"},
    "data": list(c)
}

r = json.dumps(result, default=date_encoder)

pprint.pprint(r)