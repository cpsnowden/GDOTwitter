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
p1 = {"$project": p1}
p2 = {"$project": p2}
g1 = {"$group": {"_id": "$date", "count": {"$sum": 1}}}
s1 = {"$sort": {"_id": 1}}

p3 = {"$project":{"dt":"$_id","count":"$count","_id":0}}
# p3 = {}
c = db_col.aggregate([p1, p2, g1, s1 ,p3], allowDiskUse=True)

result = {
    "details": {"chartType": "line"},
    "data": [{"_id": "ALL", "data":list(c)}]
}

r = json.dumps(result, default=date_encoder)

pprint.pprint(r)