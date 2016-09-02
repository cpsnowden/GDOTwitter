import logging
import pycountry
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

        query = [{"$match": self.time_bound_aggr()},
                 {"$group": {"_id": lang_key, "count": {"$sum": 1}}},
                 {"$sort": {"count": -1}}]

        data = list(self.col.aggregate(query, allowDiskUse=True))

        for entry in data:
            try:
                entry["_id"] = pycountry.languages.get(iso639_1_code=entry["_id"]).name
            except KeyError:
                continue

        self.export_html(result=data,
                         properties={"chartProperties": {"caption": self.dataset_meta.description,
                                                         "subcaption": "Languages from " +
                                                                       str(self.args["startDateCutOff"]) + " to " +
                                                                       str(self.args["endDateCutOff"])},
                                     "analysisType": "proportion",
                                     "chartType": "doughnut3d"},
                         export_type="chart")
        self.export_json(data)
        return True
