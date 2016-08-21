from pymongo import MongoClient
MongoClient().get_database().coll
# client = MongoClient("146.169.32.151", 27017)
#
# db = client.get_database("DATA")
# auth = db.authenticate("twitterApplication", "gdotwitter", source="admin")
# col = db.get_collection("Twitter_Brexit_GNIP")

import json

path = "gnip_top_users.json"

with open(path) as f:
    data = json.load(f)

users = [i["_id"]["user-id"] for i in data[:1000]]
# users = [i["_id"]["user-id"] for i in data if i["count"] >= 150]
print len(users)
print users[:10]

a = raw_input("Press to continue")

# client = MongoClient("localhost", 27017)
# db = client.get_database("DATA")
# auth = db.authenticate("twitterApplication", "gdotwitter", source="admin")
# col = db.get_collection("BrexitRemain_old")

client = MongoClient("146.169.32.151", 27017)
db = client.get_database("DATA")
auth = db.authenticate("twitterApplication", "gdotwitter", source="admin")
col = db.get_collection("Twitter_Brexit_GNIP")

sample_query = [
    {"$match": {"user-id": {"$in": users}}},
    {"$sample": {"size": 100000}},
    {"$out": "GNIP_50000_sample_top1000users"}
]

print "Executing query"
cursor = col.aggregate(sample_query, allowDiskUse=True)

print "Done"
