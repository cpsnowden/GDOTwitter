from pymongo import MongoClient
import pprint
from pymongo import ASCENDING
db = MongoClient().get_database("DATA").get_collection("Twitter_Breixt_9month")

cur = db.aggregate([{ "$group": { "_id": { "id": "$id" },
                            "uniqueIds": { "$addToSet": "$_id" },
                            "count": { "$sum": 1 } } },
              { "$match": { "count": { "$gt": 1 } } }], allowDiskUse=True)

duplicateIds = list(cur)

pprint.pprint(duplicateIds)
raw_input("Any button to remove")

for doc in duplicateIds:
    index = 1
    print doc["uniqueIds"]
    while index < doc["uniqueIds"].length:
        db.delete_one(doc["uniqueIds"][index])
        index += 1
    print index
    print


print db.createIndex({"id":ASCENDING},unique=True)
print "Done"