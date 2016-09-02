import logging

from AnalysisEngine import Util
from AnalysisEngine.Analytics.Analytics import Analytics
from AnalysisEngine.TwitterObj import Status, User


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
        retweet_exists_key = Status.SCHEMA_MAP[self.schema]["retweeted_status_exists"]
        user_name_key = Util.dollar_join_keys(retweet_key,
                                              Status.SCHEMA_MAP[self.schema]["retweet_user"],
                                              User.SCHEMA_MAP[self.schema]["retweet_screen_name"])

        query = [{"$match": self.time_bound_aggr()},
                 {"$match": {retweet_exists_key: {"$exists": True, "$ne": None}}},
                 {"$group": {"_id": user_name_key, "count": {"$sum": 1}}},
                 {"$sort": {"count": -1}},
                 {"$limit": limit}]

        data = list(self.col.aggregate(query, allowDiskUse=True))

        self.export_html(result=data,
                         properties={"chartProperties": {"yAxisName": "Number of Retweeted Statuses",
                                                         "xAxisName": "User",
                                                         "caption": self.dataset_meta.description,
                                                         "subcaption": "Top " + str(limit) + " retweeted users"},
                                     "analysisType": "ranking",
                                     "chartType": "bar2d"},
                         export_type="chart")
        self.export_json(data)
        return True