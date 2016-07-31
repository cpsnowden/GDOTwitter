import logging

import pandas as pd

from AnalyticsService.Analytics.Analytics import Analytics
from AnalyticsService.Analytics.BasicStats.Hashtags import Hashtags
from AnalyticsService.TwitterObj import Status
import json
from dateutil.tz import tzutc
import numpy as np
UTC = tzutc()

class HashtagTimeDistribution(Analytics):
    _logger = logging.getLogger(__name__)

    _options = {
        "Minute": "min",
        "Hour": "H",
        "Day": "D",
        "Week": "W",
        "Month": "M"
    }

    __type_name = "Hashtag Time Distribution"
    __arguments = [{"name": "timeInterval", "prettyName": "Time interval", "type": "enum", "options": _options.keys(),
                    "default": "Hour"},
                   {"name": "hashtagLimit", "prettyName": "Number of top hashtags", "type": "integer", "default": 10}]

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(HashtagTimeDistribution, cls).get_args()

    @classmethod
    def get_type(cls):
        return cls.__type_name

    ####################################################################################################################

    @classmethod
    def get(cls, analytics_meta, gridfs, db_col, args, schema_id):

        time_interval = args["timeInterval"]
        limit = args["hashtagLimit"]

        try:
            time_quantum = cls._options[time_interval]
        except KeyError:
            cls._logger.exception("Wrong time quantum given")
            return False

        data = cls.get_hashtag_time_series(schema_id, db_col, limit, time_quantum)

        cls.export_json(analytics_meta, data, gridfs)

        return True

    @classmethod
    def get_hashtag_time_series(cls, schema_id, db_col, limit, time_quantum):

        cls._logger.info("Getting hashtag time series")
        top_hashtags_list = Hashtags.get_top_hashtags(schema_id, limit, db_col)
        print top_hashtags_list
        top_hashtags = set([i['_id'].lower() for i in top_hashtags_list] + ["_ALL"])
        cls._logger.info("Found top hashtags and converted to set %s", top_hashtags)

        cursor = db_col.find({},{Status.SCHEMA_MAP[schema_id]["created_at"]: 1,
                                 Status.SCHEMA_MAP[schema_id]["hashtags"]: 1})

        used = dict([(i, []) for i in top_hashtags])
        dates = []
        for c in cursor:
            s = Status(c, schema_id)
            dates.append(s.get_created_at())
            found_htags = [h.lower() for h in s.get_hashtags()]
            for h in top_hashtags:
                if h == "_ALL":
                    continue
                if h in found_htags:
                    used[h].append(1.0)
                else:
                    used[h].append(0.0)
            used["_ALL"].append(1.0)

        index = pd.DatetimeIndex(dates)
        df = pd.DataFrame(used, index=index, columns=top_hashtags)
        gb = df.groupby(pd.TimeGrouper(freq=time_quantum)).sum()
        gb.fillna(0.0, inplace=True)
        gdb = '{"details":{"chartType":"line"},"data":' + gb.to_json(date_format='iso') + "}"

        return gdb