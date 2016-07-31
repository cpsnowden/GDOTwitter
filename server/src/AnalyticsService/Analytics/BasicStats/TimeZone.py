import json
import logging

from AnalyticsService.TwitterObj import User, Status
from AnalyticsService.Analytics.Analytics import Analytics

class TimeZone(Analytics):
    _logger = logging.getLogger(__name__)

    __type_name = "Time Zone Distribution"
    __arguments = []

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(TimeZone, cls).get_args()

    @classmethod
    def get_type(cls):
        return cls.__type_name

    ####################################################################################################################

    @classmethod
    def get(cls, analytics_meta, gridfs, db_col, args, schema_id):

        cls._logger.info("Attempting to get timezones")

        utc_offset_key = cls.dollar_join_keys(Status.SCHEMA_MAP[schema_id]["user"],
                                              User.SCHEMA_MAP[schema_id]["utc_offset"])
        print utc_offset_key
        query = [{"$group": {"_id": utc_offset_key, "count": {"$sum": 1}}},
                 {"$sort": {"count": -1}}]

        utc_offsets = db_col.aggregate(query, allowDiskUse=True)

        utc_offsets = list(utc_offsets)
        for c in utc_offsets:
            if c["_id"] is None or c["_id"] == -1:
                c["_id"] = "Unspecified"
            elif c["_id"] < 0:
                c["_id"] = "UTC" + str(float(c['_id']) / (60.0*60.0))
            elif c["_id"] > 0:
                c["_id"] = "UTC+" + str(float(c['_id']) / (60.0 * 60.0))
            elif c["_id"] == 0:
                c["_id"] = "UTC"

        data = {"details": {"chartType":"pie"}, "data":utc_offsets}

        cls.export_json(analytics_meta, json.dumps(data), gridfs)

        return True