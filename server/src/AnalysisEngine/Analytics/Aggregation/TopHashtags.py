import logging

from AnalysisEngine import Util
from AnalysisEngine.Analytics.Analytics import Analytics
from AnalysisEngine.TwitterObj import Status


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

        data = self.get_top_hashtags(self.schema, limit, self.col, self.time_bound_aggr)

        self.export_html(result=data,
                         properties={"chartProperties": {"yAxisName": "Number of Occurences",
                                                         "xAxisName": "Hashtag",
                                                         "caption": self.dataset_meta.description,
                                                         "subcaption": "Top " + str(limit) + " hashtags from " +
                                                                       str(self.args["startDateCutOff"]) + " to " +
                                                                           str(self.args["endDateCutOff"])},
                                     "analysisType": "ranking",
                                     "chartType": "bar2d"},
                         export_type="chart")
        self.export_json(data)
        return True

    @staticmethod
    def get_top_hashtags(schema, limit, col, time_bound):

        hashtag_key = Util.dollar_join_keys(Status.SCHEMA_MAP[schema]["hashtags"])
        query = [
            {"$match": time_bound()},
            {"$unwind":  hashtag_key},
            {"$group": {"_id": {"$toLower": hashtag_key + '.' + 'text'}, "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": limit}]

        return list(col.aggregate(query, allowDiskUse=True))