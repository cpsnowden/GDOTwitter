import json
import logging

from AnalysisEngine import Util
from AnalysisEngine.TwitterObj import Status
from AnalyticsService.Analytics.Analytics import Analytics
from AnalyticsService.Analytics.BasicStats.Hashtags import Hashtags


class TD_Hashtags(Analytics):
    _logger = logging.getLogger(__name__)

    _options = ["Minute", "Hour", "Day", "Week"]

    __type_name = "Hashtag Tweet Time Distribution"
    __arguments = [{"name": "timeInterval", "prettyName": "Time interval", "type": "enum", "options": _options,
                    "default": "Hour"},
                   {"name": "hashtagLimit", "prettyName": "Number of top hashtags", "type": "integer", "default": 10}]

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(TD_Hashtags, cls).get_args()

    @classmethod
    def get_type(cls):
        return cls.__type_name

    ####################################################################################################################

    @classmethod
    def get(cls, analytics_meta, gridfs, db_col, args, schema_id):

        time_interval = args["timeInterval"]
        limit = args["hashtagLimit"]

        if time_interval not in cls._options:
            cls._logger.exception("Wrong time quantum given")
            return False

        top_hashtags_list = Hashtags.get_top_hashtags(schema_id, limit, db_col)
        print top_hashtags_list
        top_hashtags = list(set([i['_id'] for i in top_hashtags_list] + ["_ALL"]))

        date_field = "$" + Status.SCHEMA_MAP[schema_id]["ISO_date"]
        hashtag_key = Status.SCHEMA_MAP[schema_id]["hashtags"]
        hashtag_dollar_key = cls.dollar_join_keys(hashtag_key)
        hashtag_dollar_text_key = cls.dollar_join_keys(hashtag_key, "text")

        uw = {"$unwind": hashtag_dollar_key}
        m = {"$match": {"hashtag":{"$in": top_hashtags}}}
        p1, p2 = Util.get_date_projection(date_field, time_interval)
        p1["hashtag"] = {"$toLower": hashtag_dollar_text_key}
        p2["hashtag"] = "$hashtag"

        g1 = {"$group": {"_id": {"dt": "$date", "series":"$hashtag"},"count": {"$sum": 1}}}
        s1 = {"$sort": {"_id.dt": 1}}
        p3 = {"$group": {"_id": "$_id.series", "data": {"$push": {"dt": "$_id.dt", "count": "$count"}}}}
        c = db_col.aggregate([uw, {"$project": p1}, m, {"$project": p2},g1,s1,p3], allowDiskUse = True)

        result_lst = list(c)
        x_values = set()
        for l in result_lst:
            for x in l["data"]:
                x_values.add(x["dt"])

        result = {"details": {"chartType": "msline",
                            "chartProperties":{"yAxisName":"Tweets per " + time_interval.lower(),
                                             "xAxisName":"Date (UTC)",
                                             "caption":"Top " + str(limit) + " hashtag time interval",
                                             "labelStep": int(len(x_values) / 20.0)}},
                  "data": {"categories": sorted(x_values), "values": result_lst}}

        cls.create_chart(gridfs, analytics_meta, result)
        cls.export_json(analytics_meta, json.dumps(result, default = Util.date_encoder), gridfs)

        return True
