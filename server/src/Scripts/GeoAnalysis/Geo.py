from AnalysisEngine.TwitterObj import Status
from AnalysisEngine.GeoAnalysis.StatusMarker import StatusMarker
import json
import sys
reload(sys)  # just to be sure
sys.setdefaultencoding('utf-8')

from pymongo import MongoClient
import json

client = MongoClient("146.169.32.151", 27017)
db = client.get_database("DATA")
auth = db.authenticate("twitterApplication", "gdotwitter", source="admin")
col = db.get_collection("Twitter_Brexit_GNIP")
schema = "GNIP"

cursor = col.find({"entities-user-place-coordinates":{"$exists":True},"entities-user-place-coordinates.lat":{
    "$ne":None}}).limit(10000)

markers = []

for i,c in enumerate(cursor):
    s = Status(c, schema)



    sm = StatusMarker(s.get_id())
    sm.text = s.get_text()
    sm.user_pic = s.get_user().get_image_url()
    sm.date = s.get_created_at()

    co = s.get_coordinates()
    sm.latitude = co.get_latitude()
    sm.longitude = co.get_longitude()
    sm.retweet_count = s.get_n_retweeted()
    sm.user_name = s.get_user().get_real_name()
    sm.user_screen_name = s.get_user().get_name()

    if(s.get_retweet_status() is not None):
        sm.retweeted_author = s.get_retweet_status().get_user(True).get_name()
    # print sm.__dict__
    markers.append(sm.jsonify())
    print i

with open("user_coordinates10000.json","w") as f:
    json.dump(markers, f)