import logging

from AnalysisEngine import Util
from AnalysisEngine.Analytics.Analytics import Analytics
from AnalysisEngine.TwitterObj import Status


class Languages(Analytics):
    _logger = logging.getLogger(__name__)
    __arguments = []

    def __init__(self, analytics_meta):
        super(Languages, self).__init__(analytics_meta)

    @classmethod
    def get_type(cls):
        return "Languages"

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(Languages, cls).get_args()

    def process(self):

        lang_key = Util.dollar_join_keys(Status.SCHEMA_MAP[self.schema]["language"])

        query = [
            {"$group": {"_id": lang_key, "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}]

        data = self.col.aggregate(query, allowDiskUse=True)

        result = {"details": {"chartType": "doughnut3d",
                              "chartProperties": {"caption": self.dataset_meta.description,
                                                  "subcaption": "Languages"}},
                  "data": list(data)}

        self.export_chart(result)
        self.export_json(result)

        return True