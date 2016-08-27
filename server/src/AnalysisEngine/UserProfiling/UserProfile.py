import datetime
import pandas as pd
import numpy as np
from AnalysisEngine.Classification.TweetClassifier.Basic import Basic


class UserProfile(object):
    def __init__(self, screenName, dataSetName, a_label, b_label, hashtags,
                 n_tweets_to_display):
        self.profileImage = None
        self.name = ""
        self.screenName = "@" + screenName
        self.description = ""
        self.createdAt = datetime.datetime.now()
        self.tweets = []
        self.marker = []
        self.no_original = 0
        self.no_retweets = 0
        self.no_friends = 0
        self.no_followers = 0
        self.n_tweets_to_display = n_tweets_to_display
        self.n_tweets = 0
        self.a_total = 0
        self.a_label = a_label
        self.b_total = 0
        self.b_label = b_label
        self.classifier = Basic(None, hashtags)
        self.timeDist = []
        self.dataSetName = dataSetName
        self.timestamp = datetime.datetime.now()

        self.timeZone = None
        self.location = ""

    def get_tweets_to_display(self):
        return self.tweets[:self.n_tweets_to_display]

    def add_tweet(self, s):
        self.n_tweets += 1
        entry = {"dt": s.get_created_at(), "text": s.get_text().replace("\n", "")}
        if s.get_retweet_status() is not None:
            entry["retweet_author"] = s.get_retweet_status().get_user(True).get_name()
        else:
            entry["retweet_author"] = ""

        cs = self.classifier.predict(s)
        if cs.classification < 0:
            self.a_total += 1
        elif cs.classification > 0:
            self.b_total += 1

        self.tweets.append(entry)

        coordinates = s.get_coordinates()
        if coordinates is not None:
            print coordinates.item.item
            if coordinates.get_latitude() is not None and coordinates.get_longitude() is not None:
                self.marker.append({"position": {"lat": float(coordinates.get_latitude()),
                                                 "lng": float(coordinates.get_longitude())},
                                    "title": s.get_created_at().strftime("%c")})

    def process_time_dist(self, time_interval):

        index = pd.DatetimeIndex(i["dt"] for i in self.tweets)
        df = pd.DataFrame(np.ones(len(index)), index=index)
        gb = df.groupby(pd.TimeGrouper(freq=time_interval)).sum()
        gb.fillna(0.0, inplace=True)
        data_dict = gb[0].to_dict()
        self.timeDist = [{"label": dt.to_pydatetime().strftime("%c"), "value": count} for (dt, count) in
                         data_dict.iteritems()]
