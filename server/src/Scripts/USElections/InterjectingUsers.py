from pymongo import MongoClient
import json
from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer
from itertools import permutations

from AnalysisEngine.Classification.TweetClassifier.SVM import TweetPreprocessor


tb = Blobber(tokenizer=TweetPreprocessor(), analyzer=NaiveBayesAnalyzer())

client = MongoClient()
db = client.get_database("DATA")
auth = db.authenticate("twitterApplication", "gdotwitter", source="admin")
col = db.get_collection("Trump_Clinton_Saunders_old")


interjecting_users = json.load(open("Scripts/USElections/WrongUsers.json"))


users = [i["user"] for i in interjecting_users]

user_map = dict((i["user"],(i["class"],i["louvian"])) for i in interjecting_users)

cursor = col.find({"user.screen_name":{"$in":users}})

labels = ["Saunders","Clinton","Trump"]
cross_labels = permutations(labels, 2)
tweets = dict([(i,[]) for i in cross_labels])
txt  = []
for c in cursor:
    blob = tb(c["text"])
    sm = blob.sentiment
    txt.append((c["text"].replace("\n",""),user_map[c["user"]["screen_name"]]))
    classification, louvian = user_map[c["user"]["screen_name"]]

    tweets[(classification,louvian)].append(c)

    print c["user"]["screen_name"], user_map[c["user"]["screen_name"]] ,c["text"].replace("\n","")

from collections import Counter

print Counter(txt).most_common(10)

clintonSaundersHashtags = []
for i in tweets[("Clinton", "Saunders")]:
    clintonSaundersHashtags += [j["text"] for j in i["entities"]["hashtags"]]
cs_htags  = Counter(clintonSaundersHashtags)
print cs_htags.most_common(4)

clintonTrumpHashtags = []
for i in tweets[("Clinton", "Trump")]:
    clintonTrumpHashtags += [j["text"] for j in i["entities"]["hashtags"]]
ct_htags  = Counter(clintonTrumpHashtags)
print ct_htags.most_common(4)