import logging
import os
import re
from collections import OrderedDict
from datetime import datetime
from datetime import timedelta

import numpy as np
import pandas as pd
from dateutil import parser
from nltk.corpus import stopwords

from AnalysisEngine import Util
from AnalysisEngine.GuardianAPI.GuardianWrapper import GuardianWrapper
from AnalysisEngine.TwitterObj import Status


class Event(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.top_words = []
        self.guardian_titles = []
        self.midpoint = self.start + (self.end - self.start) / 2

    def __str__(self):
        return "(" + str(self.midpoint) + "," + str(self.end) + ", words: " + str(self.top_words) + ", guardian: " + \
               str(self.guardian_titles) + ")"

    def __repr__(self):
        return self.__str__()

    def get_chart_label(self):
        return self.start.strftime("%a%e%b") + " {br} Top words: " + ", ".join(self.top_words) + \
               " {br}  Guardian Headlines: " + ", " + ", ".join(self.guardian_titles)


class EventDetection(object):
    _logger = logging.getLogger(__name__)

    def __init__(self, col, guardian_key):
        self.guardian_api = GuardianWrapper(guardian_key)
        self.col = col
        self.stopwords = stopwords.words('english')

    def get_top_words(self, start_date, end_date, hashtag, schema):
        self._logger.info("Getting top words for period from: %s to: %s hashtag: %s", start_date, end_date, hashtag)

        hashtag_key = Util.join_keys(Status.SCHEMA_MAP[schema]["hashtags"], "text")

        query = [
            {"$match": {"ISO_created_at": {"$gte": start_date,
                                           "$lte": end_date}}},
            {"$match": {hashtag_key: {"$in": [re.compile("^" + hashtag, re.IGNORECASE)]}}},
            {"$unwind": "$tokens-wo-stopwords"},
            {"$group": {"_id": "$tokens-wo-stopwords", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]

        top_words = self.col.aggregate(query, allowDiskUse=True)
        top_words = list(top_words)
        return [i["_id"] for i in top_words if i["_id"] not in set(self.stopwords + ["RETWEET", "RT"])]

    def find_events(self, tweet_rates, alpha=1.2, padding=2):

        df = pd.DataFrame.from_dict(tweet_rates, orient="index")
        df.columns = ["count"]

        ma = pd.rolling_mean(df, 24)
        stdev = df["count"].std()
        threshold = df["count"].mean() + pd.rolling_std(df["count"], 24)
        df["limit"] = ma + alpha * stdev
        df["event"] = (df["count"] > df["limit"]) & (df["count"] > (threshold))
        df["block"] = (df["event"].shift(1) != df["event"]).astype(int).cumsum()

        event_flags = df.reset_index().groupby(['event', 'block'])['index'].apply(lambda x: np.array(x))
        if True not in event_flags.index:
            return []

        return [Event(datetime.utcfromtimestamp(K[0].tolist() / 1e9) - timedelta(hours=padding),
                      datetime.utcfromtimestamp(K[-1].tolist() / 1e9) + timedelta(hours=padding)) for
                K in
                event_flags.ix[True]]

    def map_events(self, tweet_rates, hashtag, schema):
        events = self.find_events(tweet_rates)
        self._logger.info("Found " + str(len(events)) + " events ")

        for event in events:
            print event
            event.top_words = self.get_top_words(event.start, event.end, hashtag, schema)
            event.guardian_titles = self.guardian_api.query_topics(event.top_words,
                                                                   event.start, event.end)[:5]
            print event

        return events


if __name__ == "__main__":

    import json
    from pymongo import MongoClient
    from AnalysisEngine.HTMLGeneration.FusionCharting import get_fusion_chart_data, get_fusion_html
    #
    # data = json.load(open(os.path.join(os.path.dirname(__file__), "DATA/strongerin.json")))
    # htag = "strongerin"
    #
    data = json.load(open(os.path.join(os.path.dirname(__file__), "DATA/leave.json")))
    htag = "voteleave"
    # data = json.load(open(os.path.join(os.path.dirname(__file__), "DATA/brexit.json")))
    # htag = "brexit"

    client = MongoClient("146.169.32.151", 27017)
    db = client.get_database("DATA")
    auth = db.authenticate("twitterApplication", "gdotwitter", source="admin")
    col = db.get_collection("Twitter_Brexit_GNIP")
    ed = EventDetection(col, "4d547cbd-99e2-4b00-a40e-987c67c252b8")

    print "Getting events"
    events = ed.map_events(OrderedDict([(parser.parse(i[0]), i[1]) for i in data]), htag, "GNIP")

    json.dump({"event":[i.__dict__ for i in events],"data":data}, open("voteleave_events.json","w"),
              default=Util.date_encoder)
    #
    # fcd = get_fusion_chart_data({"series": [[parser.parse(i[0]), i[1]] for i in data], "events": events},
    #                             {"yAxisName": "Tweets per hour",
    #                              "xAxisName": "Date (UTC)",
    #                              "caption": "Brexit",
    #                              "subcaption": "'#" + htag + "'" + " event dectection",
    #                              "labelStep": int(len(data) / 20.0)},
    #                             "event",
    #                             "line")
    # html = get_fusion_html(fcd["dataSource"], fcd["chartType"])
    # with open("out3.html", "w") as f:
    #     f.write(html)
