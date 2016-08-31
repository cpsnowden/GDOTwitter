from pymongo import MongoClient

client = MongoClient("127.0.0.1", 27018)
db = client.get_database("Meta")
auth = db.authenticate("twitterApplication","gdotwitter", source = "admin")
#
# print auth
print client.get_database("Meta").collection_names()
# print client.get_database("DATA").get_collection("Brexit_old").count()


col = db.get_collection("analytics_meta")

# for c in col.find():
#
#     if "trial" in c:
#         col.update_one({"_id":c["_id"]},{"$set":{"trial":c["trial"] + ".g"}})
#
#     print c

for c in col.find():
    raw_input("Press Enter to run")
    print c["_id"]
    if "html_id" in c:
        print "Updating html"
        col.update_one({"_id": c["_id"]}, {"$set": {"html_id": c["html_id"] + ".html"}})
    if "raw_id" in c:
        print "Updating raw"
        col.update_one({"_id": c["_id"]}, {"$set": {"raw_id": c["raw_id"] + ".json"}})
    if "graph_id" in c:
        print "Updating graph"
        col.update_one({"_id": c["_id"]}, {"$set": {"graph_id": c["graph_id"] + ".graphml"}})
    if "chart_id" in c:
        print "Updating chart"
        col.update_one({"_id": c["_id"]}, {"$set": {"chart_id": c["chart_id"] + ".json"}})