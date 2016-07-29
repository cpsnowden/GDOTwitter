import logging

import pandas as pd

from AnalyticsService.Analytics.Analytics import Analytics
from AnalyticsService.TwitterObj import Status, User


class TimeZoneTimeDist(Analytics):
    _logger = logging.getLogger(__name__)

    _options = {
        "Minute": "min",
        "Hour": "H",
        "Day": "D",
        "Week": "W",
        "Month": "M"
    }

    __type_name = "Time Zone Time Distribution"
    __arguments = [{"name": "timeInterval", "prettyName": "Time interval", "type": "enum", "options": _options.keys(),
                    "default": "Hour"}]

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(TimeZoneTimeDist, cls).get_args()

    @classmethod
    def get_type(cls):
        return cls.__type_name

    ####################################################################################################################

    @classmethod
    def get(cls, analytics_meta):

        gridfs, db_col, args, schema_id = cls.setup(analytics_meta)

        time_interval = args["timeInterval"]

        try:
            time_quantum = cls._options[time_interval]
        except KeyError:
            cls._logger.exception("Wrong time quantum given")
            return False

        dates = []
        time_zones = {}
        utc_offset_key = cls.join_keys(Status.SCHEMA_MAP[schema_id]["user"],
                                       User.SCHEMA_MAP[schema_id]["utc_offset"])

        for c in db_col.find({utc_offset_key: {"$nin": [None, -1]}},
                             {Status.SCHEMA_MAP[schema_id]["created_at"]: 1,
                              utc_offset_key: 1}):

            s = Status(c, schema_id)
            utc_offset_n = s.get_user().get_utc_offset()
            if utc_offset_n is None:
                cls._logger.warning("Found None utc offset")
                continue

            utc_offset_n = float(utc_offset_n) / (60 * 60)

            if utc_offset_n < 0:
                utc_offset = "UTC" + str(utc_offset_n)
            elif utc_offset_n == 0:
                utc_offset = "UTC"
            else:
                utc_offset = "UTC+" + str(utc_offset_n)

            if utc_offset not in time_zones.keys():
                length = len(dates)
                time_zones[utc_offset] = [0] * length
            for tz in time_zones.keys():
                if tz == utc_offset:
                    time_zones[tz].append(1)
                else:
                    time_zones[tz].append(0)

            dates.append(s.get_created_at())

        index = pd.DatetimeIndex(dates)

        df = pd.DataFrame(time_zones, index=index)
        gb = df.groupby(pd.TimeGrouper(freq=time_quantum)).sum()

        gb.fillna(0.0, inplace=True)
        gdb = '{"details":{"chartType":"line"},"data":' + gb.to_json(date_format='iso') + "}"

        cls.export_json(analytics_meta, gdb, gridfs)

        return True
