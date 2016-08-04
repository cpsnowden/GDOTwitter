import json
import logging

from AnalyticsService.TwitterObj import Status
from AnalyticsService.Analytics.Analytics import Analytics

class Original(Analytics):
    _logger = logging.getLogger(__name__)

    __type_name = "Retweet vs Original"
    __arguments = []

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(Original, cls).get_args()

    @classmethod
    def get_type(cls):
        return cls.__type_name

    ####################################################################################################################

    @classmethod
    def get(cls, analytics_meta, gridfs, db_col, args, schema_id):

        cls._logger.info("Attempting to get retweet distribution")

        total = db_col.count()
        retweeted = db_col.find({Status.SCHEMA_MAP[schema_id]["retweeted_status"]: {"$exists": False}}).count()

        distribution = [{"_id":"retweets","count": retweeted},{"_id":"non_retweets","count": total - retweeted}]


        result = {"details": {"chartType": "doughnut2d",
                              "chartProperties": {"defaultCenterLabel": "Original Tweets"}},
                  "data": distribution}

        cls.create_chart(gridfs, analytics_meta, result)
        cls.export_json(analytics_meta, json.dumps(result), gridfs)

        return True