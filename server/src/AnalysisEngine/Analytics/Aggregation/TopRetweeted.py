import logging

from AnalysisEngine.Analytics.Analytics import Analytics
from AnalyticsService.TwitterObj import Status, User
from AnalyticsService import Util

class TopRetweeted(Analytics):
    _logger = logging.getLogger(__name__)
    __arguments = [dict(name="Limit", prettyName="Number of top retweeted users", type="integer",
                        default=10)]

    def __init__(self, analytics_meta):
        super(TopRetweeted, self).__init__(analytics_meta)

    @classmethod
    def get_type(cls):
        return "Top Retweeted Users"

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(TopRetweeted, cls).get_args()

    def process(self):
        limit = self.args["Limit"]

        retweet_key = Status.SCHEMA_MAP[self.schema]["retweeted_status"]
        user_name_key = Util.dollar_join_keys(retweet_key,
                                              Status.SCHEMA_MAP[self.schema]["user"],
                                              User.SCHEMA_MAP[self.schema]["name"])
        query = [
            {"$match": {retweet_key: {"$exists": True, "$ne": None}}},
            {"$group": {"_id": user_name_key, "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": limit}]

        data = self.col.aggregate(query, allowDiskUse=True)

        result = {"details": {"chartType": "bar2d",
                              "chartProperties": {"yAxisName": "Number of Retweeted Statuses",
                                                  "xAxisName": "User",
                                                  "caption": "Top " + str(limit) + " retweeted users"}},
                  "data": list(data)}

        self.export_chart(result)
        self.export_json(result)

        return True