import logging

from AnalysisEngine.Analytics.Analytics import Analytics
from AnalyticsService.TwitterObj import Status, User, UserMention
from AnalyticsService import Util

class TopMentioned(Analytics):
    _logger = logging.getLogger(__name__)
    __arguments = [dict(name="Limit", prettyName="Number of top mentioned users", type="integer",
                        default=10)]

    def __init__(self, analytics_meta):
        super(TopMentioned, self).__init__(analytics_meta)

    @classmethod
    def get_type(cls):
        return "Top Mentioned Users"

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(TopMentioned, cls).get_args()

    def process(self):
        limit = self.args["Limit"]

        mention_key = Util.dollar_join_keys(Status.SCHEMA_MAP[self.schema]["mentions"])
        user_name_key = Util.dollar_join_keys(mention_key,
                                              UserMention.SCHEMA_MAP[self.schema]["name"])

        query = [
            {"$unwind": "$" + mention_key},
            {"$group": {"_id": user_name_key, "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": limit}]

        data = self.col.aggregate(query, allowDiskUse=True)

        result = {"details": {"chartType": "bar2d",
                              "chartProperties": {"yAxisName": "Number of Times Mentioned",
                                                  "xAxisName": "User",
                                                  "caption": "Top " + str(limit) + " mentioned users"}},
                  "data": list(data)}

        self.export_chart(result)
        self.export_json(result)

        return True