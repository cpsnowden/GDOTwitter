import logging
from itertools import groupby

from AnalysisEngine.Graphing.Hashtag.HashtagGraph import HashtagGraph
from AnalysisEngine.Graphing.Community.BasicRetweet import BasicRetweet
from AnalysisEngine.Graphing.Community.RetweetCommunity import RetweetCommunity
from AnalysisEngine.Graphing.Trends.HashtagTrend import HashtagTrend
from AnalysisEngine.Graphing.Trends.HashtagTrendRetweet import HashtagTrendReweet
from AnalysisEngine.Graphing.Trends.HashtagTrendRetweet2 import HashtagTrendReweet2
from AnalysisEngine.Graphing.Trends.HashtagTrendRetweet3 import HashtagTrendReweet3

from AnalysisEngine.Analytics.TimeAggregation.TD_Sentiment import TD_Sentiment
from AnalysisEngine.Analytics.TimeAggregation.TD_Hashtag import TD_Hashtags
from AnalysisEngine.Analytics.TimeAggregation.TD_TimeZone import TD_TimeZone
from AnalysisEngine.Analytics.TimeAggregation.TD_TotalTweets import TD_TotalTweets
from AnalysisEngine.Analytics.EventDetection.HashtagEventDetection import HashtagEventDetection
from AnalysisEngine.Analytics.Aggregation.Languages import Languages
from AnalysisEngine.Analytics.Aggregation.Original import Original
from AnalysisEngine.Analytics.Aggregation.TimeZones import TimeZone
from AnalysisEngine.Analytics.Aggregation.TopAuthors import TopAuthors
from AnalysisEngine.Analytics.Aggregation.TopTweetingAuthors import TopTweetingAuthors
from AnalysisEngine.Analytics.Aggregation.TopHashtags import TopHashtags
from AnalysisEngine.Analytics.Aggregation.TopMentioned import TopMentioned
from AnalysisEngine.Analytics.Aggregation.TopRetweeted import TopRetweeted
from AnalysisEngine.Analytics.Aggregation.TopRetweeting import TopRetweeting


class AnalysisRouter():
    def __init__(self):
        pass

    _logger = logging.getLogger(__name__)

    options = [Languages,
               Original,
               TimeZone,
               TopAuthors,
               TopTweetingAuthors,
               TopMentioned,
               TopRetweeted,
               TopHashtags,
               TopRetweeting,
               TD_Sentiment,
               TD_Hashtags,
               TD_TimeZone,
               TD_TotalTweets,
               HashtagEventDetection
               ] + [
                  HashtagGraph,
                  BasicRetweet,
                  RetweetCommunity,
                  HashtagTrend,
                  HashtagTrendReweet,
                  HashtagTrendReweet2,
                  HashtagTrendReweet3]

    @classmethod
    def get_details(cls):

        return [{"classification": key,
                 "types": [{"type": o.get_type(),
                            "args": o.get_args()} for o in group]}
                for (key, group) in groupby(cls.options, lambda o: o.get_classification())]

    @classmethod
    def get_options(cls):

        return dict([(key,
                      dict([(o.get_type(),
                             o) for o in group])) for (key, group) in groupby(cls.options,
                                                                              lambda o: o.get_classification())])

    @classmethod
    def process(cls, analytics_meta):
        classification = analytics_meta.classification
        type = analytics_meta.type

        cls._logger.info("Attempting to run class: %s", analytics_meta.classification)

        try:
            analysis = cls.get_options().get(classification).get(type)
            result = analysis(analytics_meta).process()
        except Exception as e:
            cls._logger.exception("ERROR" + str(e.args) + " " + str(e))
            analytics_meta.status = "ERROR:" + str(e.args)
            analytics_meta.save()
            return False

        return result
