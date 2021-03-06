import json
import logging

from AnalysisEngine.TwitterObj import Status
from AnalyticsService.Analytics.Analytics import Analytics


class Languages(Analytics):
    _logger = logging.getLogger(__name__)

    __type_name = "Languages"
    __arguments = []

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(Languages, cls).get_args()

    @classmethod
    def get_type(cls):
        return cls.__type_name

    ####################################################################################################################

    @classmethod
    def get(cls, analytics_meta, gridfs, db_col, args, schema_id):

        cls._logger.info("Attempting to get languages")

        lang_key = Status.SCHEMA_MAP[schema_id]["language"]

        query = [
            {"$group": {"_id": '$' + lang_key, "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}]

        languages = db_col.aggregate(query, allowDiskUse=True)

        result = {"details": {"chartType": "doughnut2d",
                              "chartProperties": {"defaultCenterLabel": "Languages"}},
                  "data": list(languages)}

        cls.create_chart(gridfs,analytics_meta, result)
        cls.export_json(analytics_meta, json.dumps(result), gridfs)

        return True