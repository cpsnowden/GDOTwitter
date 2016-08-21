import logging

from AnalysisEngine import Util
from AnalysisEngine.Analytics.TimeAggregation.TimeAggregation import TimeAggregation
from AnalysisEngine.TwitterObj import Status


class TD_TotalTweets(TimeAggregation):
    _logger = logging.getLogger(__name__)
    __arguments = []

    def __init__(self, analytics_meta):
        super(TD_TotalTweets, self).__init__(analytics_meta)

    @classmethod
    def get_type(cls):
        return "Total Tweet Time Distribution"

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(TD_TotalTweets, cls).get_args()

    def process(self):
        time_interval = self.args["timeInterval"]

        date_field = Util.dollar_join_keys(Status.SCHEMA_MAP[self.schema]["ISO_date"])
        p1, p2 = Util.get_date_projection(date_field, time_interval)

        cursor = self.col.aggregate([{"$project": p1},
                                     {"$project": p2},
                                     {"$group": {"_id": "$date",
                                                 "count": {"$sum": 1}}},
                                     {"$sort": {"_id.dt": 1}},
                                     {"$project": {"dt": "$_id",
                                                   "count": "$count",
                                                   "_id": 0}}], allowDiskUse=True)

        result_lst = list(cursor)
        x_values = set()
        for l in result_lst:
            x_values.add(l["dt"])

        x_values = self.get_time_values(min(x_values), max(x_values))
        if len(x_values) > 1000:
            chartType = "zoomline"
        else:
            chartType = "msline"

        data = {"categories": sorted(x_values), "values": [{"_id": "ALL", "data": result_lst}]}

        self.export_html(result=data,
                         properties={"chartProperties": {"yAxisName": "Tweets per " + time_interval.lower(),
                                                         "xAxisName": "Date (UTC)",
                                                         "caption": self.dataset_meta.description,
                                                         "subcaption": "Tweet Rate over Time",
                                                         "labelStep": min(1, int(len(x_values) / 20.0))},
                                     "analysisType": "time",
                                     "chartType": chartType},
                         export_type="chart")
        self.export_json(data)
        return True
