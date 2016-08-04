import json
import logging

from AnalyticsService import Util
from AnalyticsService.Analytics.Analytics import Analytics
from AnalyticsService.TwitterObj import Status, User


class TD_TimeZone(Analytics):
    _logger = logging.getLogger(__name__)

    _options = ["Minute", "Hour", "Day", "Week"]

    __type_name = "TZ Time Distribution"
    __arguments = [{"name": "timeInterval", "prettyName": "Time interval", "type": "enum", "options": _options,
                    "default": "Hour"}]

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(TD_TimeZone, cls).get_args()

    @classmethod
    def get_type(cls):
        return cls.__type_name

    ####################################################################################################################

    @classmethod
    def get(cls, analytics_meta, gridfs, db_col, args, schema_id):

        time_interval = args["timeInterval"]

        if time_interval not in cls._options:
            cls._logger.exception("Wrong time quantum given")
            return False

        date_field = "$" + Status.SCHEMA_MAP[schema_id]["ISO_date"]
        utc_offset_key = cls.dollar_join_keys(Status.SCHEMA_MAP[schema_id]["user"],
                                              User.SCHEMA_MAP[schema_id]["utc_offset"])

        p1, p2 = Util.get_date_projection(date_field, time_interval)
        p1["utc_offset"] = utc_offset_key
        p2["utc_offset"] = "$utc_offset"
        g1 = {"$group": {"_id": {"dt": "$date", "series":"$utc_offset"},"count": {"$sum": 1}}}
        s1 = {"$sort": {"_id.dt": 1}}
        p3 = {"$group": {"_id": "$_id.series", "data": {"$push": {"dt": "$_id.dt", "count": "$count"}}}}

        c = db_col.aggregate([{"$project": p1}, {"$project": p2}, g1, s1, p3], allowDiskUse = True)
        result_lst = list(c)
        x_values = set()
        for l in result_lst:
            series_name = l["_id"]
            for x in l["data"]:
                x_values.add(x["dt"])
            if series_name is None or series_name == -1:
                l["_id"] = "Unspecified"
                continue
            print series_name
            series_name = float(series_name)
            if series_name < 0:
                l["_id"] = "UTC" + str(series_name / (60.0 * 60.0))
            elif series_name > 0:
                l["_id"] = "UTC+" + str(series_name / (60.0 * 60.0))
            elif series_name == 0:
                l["_id"] = "UTC"

        result = {"details": {"chartType": "msline",
                              "chartProperties": {"yAxisName": "Tweets per " + time_interval.lower(),
                                                  "xAxisName": "Date (UTC)",
                                                  "caption": "Time zone tweet rate interval",
                                                  "labelStep": min(1,int(len(x_values) / 20.0))}},
                  "data": {"categories": sorted(x_values), "values": result_lst}}

        cls.create_chart(gridfs, analytics_meta, result)

        cls.export_json(analytics_meta, json.dumps(result, default = Util.date_encoder), gridfs)

        return True
