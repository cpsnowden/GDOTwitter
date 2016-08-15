from pymongo import MongoClient
import json

client = MongoClient("146.169.32.151", 27017)
db = client.get_database("DATA")
auth = db.authenticate("twitterApplication", "gdotwitter", source="admin")
col = db.get_collection("Twitter_Brexit_GNIP")

query = [{"$group": {"_id": {"user-id": "$user-id", "user-name": "$user-preferredUsername"}, "count": {"$sum": 1}}},
         {"$sort": {"count": -1}}]
print "Starting query"
data = col.aggregate(query, allowDiskUse=True)
print "Finshed query"
with open("gnip_top_users", "w") as f:
    json.dump(list(data), f)
print "Finished saving"