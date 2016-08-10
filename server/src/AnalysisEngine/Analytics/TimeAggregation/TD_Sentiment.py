import logging

import pandas as pd
from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer

from AnalysisEngine.Analytics.TimeAggregation.TimeAggregation import TimeAggregation
from AnalysisEngine.Classification.TweetClassifier.SVM import TweetPreprocessor
from AnalysisEngine.TwitterObj import Status


class TD_Sentiment(TimeAggregation):
    _logger = logging.getLogger(__name__)
    __arguments = [{"name": "Limit",
                    "prettyName": "Tweet Limit (0 = No Limit)",
                    "type": "integer",
                    "default": 0}]

    _options = {
        "Minute": "min",
        "Hour": "H",
        "Day": "D",
        "Week": "W"
    }

    def __init__(self, analytics_meta):
        super(TD_Sentiment, self).__init__(analytics_meta)

    @classmethod
    def get_type(cls):
        return "Sentiment Time Distribution"

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(TD_Sentiment, cls).get_args()

    def process(self):

        tb = Blobber(tokenizer=TweetPreprocessor(), analyzer=NaiveBayesAnalyzer())

        limit = self.args["Limit"]
        time_interval = self._options.get(self.args["timeInterval"])
        self._logger.info("Using time interval %s", time_interval)
        dates = []
        sentiment = {"pos": [], "neg": [], "unknown": []}

        query = self.get_time_bounded_query({})
        cursor = self.get_sorted_cursor(query, limit, {Status.SCHEMA_MAP[self.schema]["created_at"]: 1,
                                                       Status.SCHEMA_MAP[self.schema]["text"]: 1})

        if cursor is None:
            self.analytics_meta.status = "NO DATA IN RANGE"
            self.analytics_meta.save()
            return False

        for c in cursor:
            s = Status(c, self.schema)
            dates.append(s.get_created_at())
            blob = tb(s.get_text())
            sm = blob.sentiment
            sent = sm.classification
            for s in sentiment.keys():
                if s == sent:
                    sentiment[s].append(1)
                else:
                    sentiment[s].append(0)

        index = pd.DatetimeIndex(dates)
        df = pd.DataFrame(sentiment, index=index)
        gb = df.groupby(pd.TimeGrouper(freq=time_interval)).sum()
        gb.fillna(0.0, inplace=True)

        data_dict = gb.to_dict()
        data = [{"_id": series_name,
                 "data": [{"dt": dt,
                           "count": count} for (dt, count) in series_data.iteritems()]}
                for (series_name, series_data) in data_dict.iteritems()]
        x_values = gb.index.tolist()

        if len(x_values) > 1000:
            chartType = "zoomline"
        else:
            chartType = "msline"

        result = {"details": {"chartType": chartType,
                              "chartProperties": {"yAxisName": "Tweets per " + time_interval.lower(),
                                                  "xAxisName": "Date (UTC)",
                                                  "caption": self.dataset_meta.description,
                                                  "subcaption": "Sentiment Time Distribution",
                                                  "labelStep": int(len(x_values) / 20.0)}},
                  "data": {"categories": sorted(x_values), "values": data}}

        self.export_chart(result)
        self.export_json(result)

        return True
