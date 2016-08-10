import logging

from AnalysisEngine.Analytics.Analytics import Analytics
from AnalysisEngine.TwitterObj import Status


class Original(Analytics):
    _logger = logging.getLogger(__name__)
    __arguments = []

    def __init__(self, analytics_meta):
        super(Original, self).__init__(analytics_meta)

    @classmethod
    def get_type(cls):
        return "Original"

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(Original, cls).get_args()

    def process(self):

        total = self.col.count()
        retweeted = self.col.find({Status.SCHEMA_MAP[self.schema]["retweet_exists_key"]: {"$exists": True, "$ne": None}}).count()

        distribution = [{"_id": "retweets", "count": retweeted}, {"_id": "non_retweets", "count": total - retweeted}]

        result = {"details": {"chartType": "doughnut3d",
                              "chartProperties": {"caption": self.dataset_meta.description,
                                                  "subcaption": "Original Tweets"}},
                  "data": distribution}

        self.export_chart(result)
        self.export_json(result)

        return True