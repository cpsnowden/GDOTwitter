import logging

from AnalysisEngine import Util
from AnalysisEngine.Analytics.TimeAggregation.TimeAggregation import TimeAggregation
from AnalysisEngine.TwitterObj import Status, User


class TD_TimeZone(TimeAggregation):
    _logger = logging.getLogger(__name__)
    __arguments = []

    def __init__(self, analytics_meta):
        super(TD_TimeZone, self).__init__(analytics_meta)

    @classmethod
    def get_type(cls):
        return "Time Zone Time Distribution"

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(TD_TimeZone, cls).get_args()

    def process(self):

        time_interval = self.args["timeInterval"]

        date_field = Util.dollar_join_keys(Status.SCHEMA_MAP[self.schema]["ISO_date"])
        utc_offset_key = Util.dollar_join_keys(Status.SCHEMA_MAP[self.schema]["user"],
                                               User.SCHEMA_MAP[self.schema]["utc_offset"])

        p1, p2 = Util.get_date_projection(date_field, time_interval)
        p1["utc_offset"] = utc_offset_key
        p2["utc_offset"] = "$utc_offset"

        cursor = self.col.aggregate([{"$project": p1},
                                     {"$project": p2},
                                     {"$group": {"_id": {"dt": "$date",
                                                         "series": "$utc_offset"},
                                                 "count": {"$sum": 1}}},
                                     {"$sort": {"_id.dt": 1}},
                                     {"$group": {"_id": "$_id.series",
                                                 "data": {"$push": {"dt": "$_id.dt",
                                                                    "count": "$count"}}}}
                                     ], allowDiskUse=True)

        result_lst = list(cursor)
        x_values = set()
        for l in result_lst:
            series_name = l["_id"]
            for x in l["data"]:
                x_values.add(x["dt"])
            if series_name is None or series_name == -1:
                l["_id"] = "Unspecified"
                continue
            series_name = float(series_name)
            if series_name < 0:
                l["_id"] = "UTC" + str(series_name / (60.0 * 60.0))
            elif series_name > 0:
                l["_id"] = "UTC+" + str(series_name / (60.0 * 60.0))
            elif series_name == 0:
                l["_id"] = "UTC"

        x_values = self.get_time_values(min(x_values), max(x_values))

        result = {"details": {"chartType": "msline",
                              "chartProperties": {"yAxisName": "Tweets per " + time_interval.lower(),
                                                  "xAxisName": "Date (UTC)",
                                                  "caption": self.dataset_meta.description,
                                                  "subcaption": "Time zone tweet rate interval",
                                                  "labelStep": min(1, int(len(x_values) / 20.0))}},
                  "data": {"categories": sorted(x_values), "values": result_lst}}

        self.export_chart(result)
        self.export_json(result)

        return True
