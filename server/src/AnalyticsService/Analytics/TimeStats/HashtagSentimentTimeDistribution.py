import logging

import pandas as pd

from AnalyticsService.Analytics.Analytics import Analytics
from AnalyticsService.Analytics.BasicStats.Hashtags import Hashtags
from AnalyticsService.TwitterObj import Status
import json
from dateutil.tz import tzutc
import numpy as np
from AnalyticsService.Graphing.Classification.TweetClassifier.SVM import TweetPreprocessor
from textblob.sentiments import NaiveBayesAnalyzer
from textblob import TextBlob, Blobber
UTC = tzutc()
from itertools import product

class HashtagSentimentTimeDistribution(Analytics):
    _logger = logging.getLogger(__name__)

    _options = {
        "Minute": "min",
        "Hour": "H",
        "Day": "D",
        "Week": "W",
        "Month": "M"
    }

    __type_name = "Hashtag Sentiment Time Distribution"
    __arguments = [{"name": "timeInterval", "prettyName": "Time interval", "type": "enum", "options": _options.keys(),
                    "default": "Hour"},
                   {"name": "hashtagLimit", "prettyName": "Number of top hashtags", "type": "integer", "default": 10}]

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(HashtagSentimentTimeDistribution, cls).get_args()

    @classmethod
    def get_type(cls):
        return cls.__type_name

    ####################################################################################################################

    @classmethod
    def get(cls, analytics_meta, gridfs, db_col, args, schema_id):

        time_interval = args["timeInterval"]
        limit = args["hashtagLimit"]

        try:
            time_quantum = cls._options[time_interval]
        except KeyError:
            cls._logger.exception("Wrong time quantum given")
            return False

        data = cls.get_hashtag_time_series(schema_id, db_col, limit, time_quantum)

        cls.export_json(analytics_meta, data, gridfs)

        return True

    @classmethod
    def get_hashtag_time_series(cls, schema_id, db_col, limit, time_quantum):
        tb = Blobber(tokenizer=TweetPreprocessor(), analyzer=NaiveBayesAnalyzer())
        cls._logger.info("Getting hashtag time series")
        top_hashtags_list = Hashtags.get_top_hashtags(schema_id, limit, db_col)

        top_hashtags = set([i['_id'].lower() for i in top_hashtags_list] + ["_ALL"])
        cls._logger.info("Found top hashtags and converted to set %s", top_hashtags)

        cursor = db_col.find({},{Status.SCHEMA_MAP[schema_id]["created_at"]: 1,
                                 Status.SCHEMA_MAP[schema_id]["hashtags"]: 1,
                                 Status.SCHEMA_MAP[schema_id]["text"]: 1})
        sentiment_labels = ["pos","neg"]
        used = dict([(i + "_" + j , []) for (i,j) in product(top_hashtags,sentiment_labels)])
        cls._logger.info("Using sentiment hashtags labels %s", used)
        dates = []
        for c in cursor:
            s = Status(c, schema_id)
            blob = tb(s.get_text())
            sent = blob.sentiment.classification
            sent_score = 1.0 if sent == "pos" else -1.0
            dates.append(s.get_created_at())
            found_htags = [h.lower() for h in s.get_hashtags()]
            for h in top_hashtags:
                if h == "_ALL":
                    continue
                if h in found_htags:
                    for l in sentiment_labels:
                        if l == sent:
                            used[h + "_" + l].append(sent_score)
                        else:
                            used[h + "_" + l].append(0.0)
                else:
                    for l in sentiment_labels:
                        if l == sent:
                            used[h + "_" + l].append(0.0)
                        else:
                            used[h + "_" + l].append(0.0)
            for l in sentiment_labels:
                if l == sent:
                    used["_ALL_" + l].append(sent_score)
                else:
                    used["_ALL_" + l].append(0.0)

        index = pd.DatetimeIndex(dates)
        df = pd.DataFrame(used, index=index, columns=used.keys())
        gb = df.groupby(pd.TimeGrouper(freq=time_quantum)).sum()
        gb.fillna(0.0, inplace=True)
        gdb = '{"details":{"chartType":"line"},"data":' + gb.to_json(date_format='iso') + "}"

        return gdb