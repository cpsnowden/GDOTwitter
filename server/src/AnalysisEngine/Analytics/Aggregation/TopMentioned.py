import logging

from AnalysisEngine import Util
from AnalysisEngine.Analytics.Analytics import Analytics
from AnalysisEngine.TwitterObj import Status, UserMention


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
        user_name_key = Util.join_keys(mention_key,
                                       UserMention.SCHEMA_MAP[self.schema]["name"])

        query = [{"$unwind": mention_key},
                 {"$group": {"_id": user_name_key, "count": {"$sum": 1}}},
                 {"$sort": {"count": -1}},
                 {"$limit": limit}]

        data = list(self.col.aggregate(query, allowDiskUse=True))

        self.export_html(result=data,
                         properties={"chartProperties": {"yAxisName": "Number of Times Mentioned",
                                                         "xAxisName": "User",
                                                         "caption": self.dataset_meta.description,
                                                         "subcaption": "Top " + str(limit) + " mentioned users"},
                                     "analysisType": "ranking",
                                     "chartType": "bar2d"},
                         export_type="chart")
        self.export_json(data)
        return True