import logging

from AnalysisEngine import Util
from AnalysisEngine.Analytics.Analytics import Analytics
from AnalysisEngine.TwitterObj import Status, User


class TimeZone(Analytics):
    _logger = logging.getLogger(__name__)
    __arguments = []

    def __init__(self, analytics_meta):
        super(TimeZone, self).__init__(analytics_meta)

    @classmethod
    def get_type(cls):
        return "Time Zone Distribution"

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(TimeZone, cls).get_args()

    def process(self):

        utc_offset_key = Util.dollar_join_keys(Status.SCHEMA_MAP[self.schema]["user"],
                                               User.SCHEMA_MAP[self.schema]["utc_offset"])

        query = [{"$group": {"_id": utc_offset_key, "count": {"$sum": 1}}},
                 {"$sort": {"count": -1}}]

        data = self.col.aggregate(query, allowDiskUse=True)

        utc_offsets = list(data)
        for c in utc_offsets:
            if c["_id"] is None or c["_id"] == -1:
                c["_id"] = "Unspecified"
            elif c["_id"] < 0:
                c["_id"] = "UTC" + str(float(c['_id']) / (60.0 * 60.0))
            elif c["_id"] > 0:
                c["_id"] = "UTC+" + str(float(c['_id']) / (60.0 * 60.0))
            elif c["_id"] == 0:
                c["_id"] = "UTC"

        result = {"details": {"chartType": "doughnut2d",
                              "chartProperties": {"defaultCenterLabel": "Time Zones"}},
                  "data": utc_offsets}

        self.export_chart(result)
        self.export_json(result)

        return True