import json
import logging

from AnalysisEngine import Util
from AnalysisEngine.TwitterObj import Status
from AnalyticsService.Analytics.Analytics import Analytics


class TD_TotalTweets(Analytics):
    _logger = logging.getLogger(__name__)

    _options = ["Minute","Hour","Day","Week"]

    __type_name = "Total Tweet Time Distribution"
    __arguments = [{"name": "timeInterval", "prettyName": "Time interval", "type": "enum", "options": _options,
                    "default": "Hour"}]

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(TD_TotalTweets, cls).get_args()

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
        p1, p2 = Util.get_date_projection(date_field, time_interval)
        g1 = {"$group": {"_id": "$date","count": {"$sum": 1}}}
        s1 = {"$sort": {"_id.dt": 1}}
        p3 = {"$project": {"dt": "$_id", "count": "$count", "_id": 0}}

        c = db_col.aggregate([{"$project": p1},{"$project": p2},g1,s1,p3], allowDiskUse = True)

        result_lst = list(c)
        x_values = set()
        for l in result_lst:
            x_values.add(l["dt"])

        result = {"details": {"chartType": "msline",
                              "chartProperties": {"yAxisName": "Tweets per " + time_interval.lower(),
                                                  "xAxisName": "Date (UTC)",
                                                  "caption": "Tweet Rate over Time",
                                                  "labelStep": min(1,int(len(x_values) / 20.0))}},
                "data": {"categories": sorted(x_values),"values":[{"_id": "ALL","data":result_lst}]}}


        cls.create_chart(gridfs, analytics_meta, result)

        cls.export_json(analytics_meta, json.dumps(result, default = Util.date_encoder), gridfs)

        return True
