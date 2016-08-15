from pymongo import MongoClient
import json
import datetime

client = MongoClient("146.169.32.151", 27017)
db = client.get_database("DATA")
auth = db.authenticate("twitterApplication", "gdotwitter", source="admin")
col = db.get_collection("Twitter_Brexit_GNIP")


start = datetime.datetime(2016,02,19,20)
end = datetime.datetime(2016,02,19,23,45)

start = datetime.datetime(2016,06,9,18)
end = datetime.datetime(2016,06,9,23,59)

start = datetime.datetime(2016,06,19,17)
end = datetime.datetime(2016,06,19,23,59)

date_query = {"ISO_created_at":{"$gte":start,"$lte":end}}
aggr = [{"$match":date_query},{"$match":{"entities-hashtags.text":{"$in":["VoteLeave","voteleave"]}}},
        {"$unwind":"$tokens-wo-stopwords"},{"$group":{"_id":"$tokens-wo-stopwords","count":{"$sum":1}}},
        {"$sort":{"count":-1}},
        {"$limit":10}]

retweeted = col.aggregate(aggr, allowDiskUse = True)
top_words = list(retweeted)
# import pprint
# pprint.pprint()

terms = [i["_id"] for i in top_words]
print terms
# c =  col.find(date_query)
# for cu in c:
#     print cu
#     break
print "End"
#
#
# query = [{"$group": {"_id": {"user-id": "$user-id", "user-name": "$user-preferredUsername"}, "count": {"$sum": 1}}},
#          {"$sort": {"count": -1}}]
# print "Starting query"
# data = col.aggregate(query, allowDiskUse=True)
# print "Finshed query"
# with open("gnip_top_users", "w") as f:
#     json.dump(list(data), f)
# print "Finished saving"

# from_date = start.strftime("%Y-%m-%d")
# to_date = end.strftime("%Y-%m-%d")

from_date = start.isoformat()
print from_date
to_date = end.isoformat()

from nltk.corpus import stopwords
terms = [i for i in terms if i not in set(stopwords.words('english') + ["RETWEET", "RT"])]

topic = " AND ".join(terms)



#
print topic
import requests
# topic = "eu referendum"
key = "4d547cbd-99e2-4b00-a40e-987c67c252b8"
# from_date = "2016-02-19"
# to_date ="2016-02-21"
url = "http://content.guardianapis.com/search?q=" + topic + "&" + "from-date=" + from_date + "&" + \
      "to-date=" + \
      to_date \
      + "&use-date=published&api-key=" + key
import json
import pprint
a = requests.get(url)
b = a.json()
pprint.pprint([i["webTitle"] for i in b["response"]["results"]])





