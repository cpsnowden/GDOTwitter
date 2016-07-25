import json
import logging

from AnalyticsService.Analytics.Analytics import Analytics
from AnalyticsService.TwitterObj import Status, User, UserMention


class TopRetweeted(Analytics):
    _logger = logging.getLogger(__name__)

    __type_name = "Top Retweeted Users"
    __arguments = [{"name":"topRetweetedLimit","prettyName":"Number of top retweeted users", "type": "integer",
                    "default": 10}]

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(TopRetweeted, cls).get_args()

    @classmethod
    def get_type(cls):
        return cls.__type_name

    ####################################################################################################################

    @classmethod
    def get(cls, analytics_meta):

        gridfs, db_col, args, schema_id = cls.setup(analytics_meta)

        retweeted_limit = args["topRetweetedLimit"]

        data = cls.get_top_retweeted(schema_id, retweeted_limit, db_col)
        result = {"details": {"chartType": "bar"}, "data": data}
        cls.export_json(analytics_meta, json.dumps(result), gridfs)

        return True


    @classmethod
    def get_top_retweeted(cls, schema_id, limit, db_col):

        cls._logger.info("Attempting to get top retweeted users")

        retweet_key = Status.SCHEMA_MAP[schema_id]["retweeted_status"]
        user_key = Status.SCHEMA_MAP[schema_id]["user"]
        user_id_key = retweet_key + "." + user_key + "." + User.SCHEMA_MAP[schema_id]["id"]
        user_name_key = retweet_key + "." + user_key + "." + User.SCHEMA_MAP[schema_id]["name"]

        top_user_query = [
            {"$match": {Status.SCHEMA_MAP[schema_id]["retweeted_status"]: {"$exists": True, "$ne": None}}},
            {"$group": {"_id": '$' + user_name_key, "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": limit}]

        top_users = db_col.aggregate(top_user_query, allowDiskUse=True)

        return list(top_users)