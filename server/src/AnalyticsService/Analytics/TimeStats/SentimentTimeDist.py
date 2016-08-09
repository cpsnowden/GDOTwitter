import logging

import pandas as pd
from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer

from AnalysisEngine.TwitterObj import Status
from AnalyticsService.Analytics.Analytics import Analytics
from AnalyticsService.Graphing.Classification.TweetClassifier.SVM import TweetPreprocessor


class SentimentTimeDistribution(Analytics):
    _logger = logging.getLogger(__name__)

    _options = {
        "Minute": "min",
        "Hour": "H",
        "Day": "D",
        "Week": "W",
        "Month": "M"
    }

    __type_name = "Sentiment Time Distribution"
    __arguments = [{"name":"timeInterval","prettyName":"Time interval","type": "enum", "options":_options.keys(),
                    "default":"Hour"}]

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(SentimentTimeDistribution, cls).get_args()


    @classmethod
    def get_type(cls):
        return cls.__type_name

    ####################################################################################################################

    @classmethod
    def get(cls, analytics_meta, gridfs, db_col, args, schema_id):

        tb = Blobber(tokenizer=TweetPreprocessor(), analyzer=NaiveBayesAnalyzer())


        time_interval = args["timeInterval"]


        try:
            time_quantum = cls._options[time_interval]
        except KeyError:
            cls._logger.exception("Wrong time quantum given")
            return False

        dates = []
        sentiment = {"pos":[],"neg":[],"unknown":[]}

        for c in db_col.find({}, {Status.SCHEMA_MAP[schema_id]["created_at"]: 1,
                                  Status.SCHEMA_MAP[schema_id]["text"]: 1}):
            s = Status(c, schema_id)
            dates.append(s.get_created_at())
            blob = tb(s.get_text())
            sm = blob.sentiment
            # print sm
            sent = sm.classification
            for s in sentiment.keys():
                if s == sent:
                    sentiment[s].append(1)
                else:
                    sentiment[s].append(0)

        index = pd.DatetimeIndex(dates)

        df = pd.DataFrame(sentiment, index=index)
        gb = df.groupby(pd.TimeGrouper(freq=time_quantum)).sum()

        # data = gb.to_json(date_format='iso')
        # gb = df.groupby(pd.TimeGrouper(freq=time_quantum)).sum()

        gb.fillna(0.0, inplace=True)
        gdb = '{"details":{"chartType":"line"},"data":' + gb.to_json(date_format='iso') + "}"


        cls.export_json(analytics_meta, gdb, gridfs)

        return True