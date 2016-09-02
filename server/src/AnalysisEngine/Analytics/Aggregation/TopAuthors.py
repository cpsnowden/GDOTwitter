import logging

from AnalysisEngine import Util
from AnalysisEngine.Analytics.Analytics import Analytics
from AnalysisEngine.TwitterObj import Status, User


class TopAuthors(Analytics):
    _logger = logging.getLogger(__name__)
    __arguments = [dict(name="Limit", prettyName="Number of top non-retweeting users", type="integer",
                        default=10)]

    def __init__(self, analytics_meta):
        super(TopAuthors, self).__init__(analytics_meta)

    @classmethod
    def get_type(cls):
        return "Top Original Authors"

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(TopAuthors, cls).get_args()

    def process(self):
        limit = self.args["Limit"]

        user_name_key = Util.dollar_join_keys(Status.SCHEMA_MAP[self.schema]["user"],
                                              User.SCHEMA_MAP[self.schema]["name"])

        query = [{"$match": self.time_bound_aggr()},
                 {"$match": {"$or": [{Status.SCHEMA_MAP[self.schema][
                                          "retweeted_status_exists"]: {"$exists": False}},
                                     {Status.SCHEMA_MAP[self.schema]["retweeted_status_exists"]: {"$eq": None}}]}},
                 {"$group": {"_id": user_name_key, "count": {"$sum": 1}}},
                 {"$sort": {"count": -1}},
                 {"$limit": limit}]

        data = list(self.col.aggregate(query, allowDiskUse=True))

        self.export_html(result=data,
                         properties={"chartProperties": {"yAxisName": "Number of Tweets",
                                                         "xAxisName": "Author",
                                                         "caption": self.dataset_meta.description,
                                                         "subcaption": "Top " + str(limit) + " original authors"},
                                     "analysisType": "ranking",
                                     "chartType": "bar2d"},
                         export_type="chart")
        self.export_json(data)
        return True
