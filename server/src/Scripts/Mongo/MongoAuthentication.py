from pymongo import MongoClient

client = MongoClient()
db = client.get_database("DATA")
auth = db.authenticate("twitterApplication","gdotwitter", source = "admin")

print auth
print client.get_database("DATA").collection_names()
print client.get_database("DATA").get_collection("Brexit_old").count()