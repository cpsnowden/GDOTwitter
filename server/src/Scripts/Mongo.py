from pymongo import MongoClient

db = MongoClient().get_database("DATA")
db.authenticate("twitterApplication","gdotwitter", source="admin")

print db.get_collection("Brexit_old").find({},{"retweetedStatus":1}).limit(1)[0]