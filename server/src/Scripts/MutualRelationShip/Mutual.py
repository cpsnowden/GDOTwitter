from pymongo import MongoClient
import json

client = MongoClient()
db = client.get_database("DATA")
auth = db.authenticate("twitterApplication", "gdotwitter", source="admin")
# col = db.get_collection("BrexitRemain_old")
col = db.get_collection("Brexit_old")


query = [
    {"$match":{"retweetedStatus.text":{"$eq":None}}},
    {"$unwind":"$userMentionEntities"},
    {"$project": {
        "_id": 1,
        "source": "$user.screenName",
        "target": "$userMentionEntities.screenName",
        "AB": {"$cond": [{"$gt": ['$userMentionEntities.screenName', '$user.screenName']},
                              1,
                              0]},
        "BA": {"$cond": [{"$lte": ['$userMentionEntities.screenName', '$user.screenName']},
                              1,
                              0]},
        "groupId": {"$cond": [{"$gt": ['$userMentionEntities.screenName', '$user.screenName']},
                              {"A": "$userMentionEntities.screenName", "B": "$user.screenName"},
                              {"A": "$user.screenName", "B": "$userMentionEntities.screenName"}]}}
    },
    # {"$group":{"_id": {"source":"$source","target":"$target"}, "A": {"$sum": 1}}},
    {"$group":{"_id":"$groupId","count": {"$sum": 1}, "AB":{"$sum":"$AB"}, "BA":{"$sum":"$BA"}}},
    {"$project":{
        "_id":1,
        "count":1,
        "AB":1,
        "BA":1,
        "Metric":{"$abs":{"$divide":[{"$multiply":["$AB","$BA"]},{"$add":["$AB","$BA"]}]}}
    }},
    # {"$match":{"Metric":{"$ne":1}}},
    {"$sort": {"Metric": -1}},
    {"$limit": 100}
]


print "Starting query"
data = col.aggregate(query, allowDiskUse=True)
# print list(data)
for d in data:
    print d

# print "Finshed query"
# with open("gnip_top_users", "w") as f:
#     json.dump(list(data), f)
# print "Finished saving"