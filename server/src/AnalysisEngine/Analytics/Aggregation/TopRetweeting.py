import logging

from AnalysisEngine import Util
from AnalysisEngine.Analytics.Analytics import Analytics
from AnalysisEngine.TwitterObj import Status, User


class TopRetweeting(Analytics):
    _logger = logging.getLogger(__name__)
    __arguments = [dict(name="Limit", prettyName="Number of top retweeting users", type="integer",
                        default=10)]

    def __init__(self, analytics_meta):
        super(TopRetweeting, self).__init__(analytics_meta)

    @classmethod
    def get_type(cls):
        return "Top Retweeting Users"

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(TopRetweeting, cls).get_args()

    def process(self):
        limit = self.args["Limit"]

        retweet_key = Status.SCHEMA_MAP[self.schema]["retweeted_status"]
        retweet_exists_key = Status.SCHEMA_MAP[self.schema]["retweeted_status_exists"]
        user_name_key = Util.dollar_join_keys(Status.SCHEMA_MAP[self.schema]["user"],
                                              User.SCHEMA_MAP[self.schema]["name"])
        query = [
            {"$match": {retweet_exists_key: {"$exists": True, "$ne": None}}},
            {"$group": {"_id": user_name_key, "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": limit}]

        data = self.col.aggregate(query, allowDiskUse=True)

        result = {"details": {"chartType": "bar2d",
                              "chartProperties": {"yAxisName": "Number of Retweets",
                                                  "xAxisName": "User",
                                                  "caption": self.dataset_meta.description,
                                                  "subcaption": "Top " + str(limit) + " retweeting users"}},
                  "data": list(data)}

        self.export_chart(result)
        self.export_json(result)

        return True