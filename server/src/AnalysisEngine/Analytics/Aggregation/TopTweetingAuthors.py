import logging

from AnalysisEngine import Util
from AnalysisEngine.Analytics.Analytics import Analytics
from AnalysisEngine.TwitterObj import Status, User


class TopTweetingAuthors(Analytics):
    _logger = logging.getLogger(__name__)
    __arguments = [dict(name="Limit", prettyName="Number of top tweeting users", type="integer",
                        default=10)]

    def __init__(self, analytics_meta):
        super(TopTweetingAuthors, self).__init__(analytics_meta)

    @classmethod
    def get_type(cls):
        return "Top Authors"

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(TopTweetingAuthors, cls).get_args()

    def process(self):
        limit = self.args["Limit"]

        user_name_key = Util.dollar_join_keys(Status.SCHEMA_MAP[self.schema]["user"],
                                              User.SCHEMA_MAP[self.schema]["name"])

        query = [
            {"$group": {"_id": user_name_key, "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": limit}]

        data = self.col.aggregate(query, allowDiskUse=True)

        result = {"details": {"chartType": "bar2d",
                              "chartProperties": {"yAxisName": "Number of Tweets",
                                                  "xAxisName": "Author",
                                                  "caption": self.dataset_meta.description,
                                                  "subcaption": "Top " + str(limit) + "tweeting authors"}},
                  "data": list(data)}

        self.export_chart(result)
        self.export_json(result)

        return True
