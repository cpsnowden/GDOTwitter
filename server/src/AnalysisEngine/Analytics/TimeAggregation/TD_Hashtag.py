import logging

from AnalysisEngine.Analytics.Aggregation.TopHashtags import TopHashtags
from AnalysisEngine.Analytics.TimeAggregation.TimeAggregation import TimeAggregation
from AnalyticsService import Util
from AnalyticsService.TwitterObj import Status


class TD_Hashtags(TimeAggregation):
    _logger = logging.getLogger(__name__)
    __arguments = [{"name": "Limit",
                    "prettyName": "Number of top hashtags",
                    "type": "integer",
                    "default": 10}]

    def __init__(self, analytics_meta):
        super(TD_Hashtags, self).__init__(analytics_meta)

    @classmethod
    def get_type(cls):
        return "Hashtag Time Distribution"

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(TD_Hashtags, cls).get_args()

    def process(self):

        limit = self.args["Limit"]
        time_interval = self.args["timeInterval"]

        top_hashtags_list = TopHashtags.get_top_hashtags(self.schema, limit, self.col)
        top_hashtags = list(set([i['_id'] for i in top_hashtags_list] + ["_ALL"]))

        date_field = Util.dollar_join_keys(Status.SCHEMA_MAP[self.schema]["ISO_date"])
        hashtag_key = Status.SCHEMA_MAP[self.schema]["hashtags"]
        hashtag_dollar_key = Util.dollar_join_keys(hashtag_key)
        hashtag_dollar_text_key = Util.dollar_join_keys(hashtag_key, "text")

        p1, p2 = Util.get_date_projection(date_field, time_interval)
        p1["hashtag"] = {"$toLower": hashtag_dollar_text_key}
        p2["hashtag"] = "$hashtag"

        cursor = self.col.aggregate([{"$unwind": hashtag_dollar_key},
                                     {"$project": p1},
                                     {"$match": {"hashtag": {"$in": top_hashtags}}},
                                     {"$project": p2},
                                     {"$group": {"_id": {"dt": "$date",
                                                         "series": "$hashtag"},
                                                 "count": {"$sum": 1}}},
                                     {"$sort": {"_id.dt": 1}},
                                     {"$group": {"_id": "$_id.series",
                                                 "data": {"$push": {"dt": "$_id.dt",
                                                                    "count": "$count"}}}}
                                     ], allowDiskUse=True)

        result_lst = list(cursor)
        x_values = set()
        for l in result_lst:
            for x in l["data"]:
                x_values.add(x["dt"])

        result = {"details": {"chartType": "msline",
                              "chartProperties": {"yAxisName": "Tweets per " + time_interval.lower(),
                                                  "xAxisName": "Date (UTC)",
                                                  "caption": "Top " + str(limit) + " hashtag time interval",
                                                  "labelStep": int(len(x_values) / 20.0)}},
                  "data": {"categories": sorted(x_values), "values": result_lst}}

        self.export_chart(result)
        self.export_json(result)

        return True
