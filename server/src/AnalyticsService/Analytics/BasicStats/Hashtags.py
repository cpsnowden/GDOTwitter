import json
import logging

from AnalyticsService.TwitterObj import Status
from AnalyticsService.Analytics.Analytics import Analytics

class Hashtags(Analytics):
    _logger = logging.getLogger(__name__)

    __type_name = "Top Hashtags"
    __arguments = [{"name":"topHashtagLimit","prettyName":"Number of top hashtags","type":"integer", "default": 10}]

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(Hashtags, cls).get_args()

    @classmethod
    def get_type(cls):
        return cls.__type_name

    ####################################################################################################################

    @classmethod
    def get(cls, analytics_meta):

        gridfs, db_col, args, schema_id = cls.setup(analytics_meta)

        hashtag_limit = args["topHashtagLimit"]

        d = cls.get_top_hashtags(schema_id, hashtag_limit, db_col)
        result = {"details": {"chartType": "bar"}, "data": d}
        cls.export_json(analytics_meta, json.dumps(result), gridfs)

        return True

    @classmethod
    def get_top_hashtags(cls, schema_id, limit, db_col):
        cls._logger.info("Attempting to get top hashtags")

        hashtag_key = Status.SCHEMA_MAP[schema_id]["hashtags"]

        top_user_query = [
            {"$unwind": "$" + hashtag_key},
            {"$group": {"_id": {"$toLower": '$' + hashtag_key + '.' + 'text'}, "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": limit}]

        top_hastags = db_col.aggregate(top_user_query, allowDiskUse=True)

        return list(top_hastags)