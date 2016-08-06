import logging

from AnalysisEngine.Analytics.Analytics import Analytics
from AnalyticsService.TwitterObj import Status
from AnalyticsService import Util

class TopHashtags(Analytics):
    _logger = logging.getLogger(__name__)
    __arguments = [dict(name="Limit", prettyName="Number of top hashtags", type="integer",
                        default=10)]

    def __init__(self, analytics_meta):
        super(TopHashtags, self).__init__(analytics_meta)

    @classmethod
    def get_type(cls):
        return "Top Hashtags"

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(TopHashtags, cls).get_args()

    def process(self):
        limit = self.args["Limit"]

        data = self.get_top_hashtags(self.schema, limit, self.col)

        result = {"details": {"chartType": "bar2d",
                              "chartProperties": {"yAxisName": "Number of Occurences",
                                                  "xAxisName": "Hashtag",
                                                  "caption": "Top " + str(limit) + " hashtags"}},
                  "data": data}

        self.export_chart(result)
        self.export_json(result)

        return True

    @staticmethod
    def get_top_hashtags(schema, limit, col):

        hashtag_key = Util.dollar_join_keys(Status.SCHEMA_MAP[schema]["hashtags"])
        query = [
            {"$unwind":  hashtag_key},
            {"$group": {"_id": {"$toLower": hashtag_key + '.' + 'text'}, "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": limit}]

        return list(col.aggregate(query, allowDiskUse=True))