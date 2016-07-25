import json
import logging

from AnalyticsService.Analytics.Analytics import Analytics
from AnalyticsService.TwitterObj import Status, User, UserMention


class TopMentioned(Analytics):
    _logger = logging.getLogger(__name__)

    __type_name = "Top Mentioned Users"
    __arguments = [{"name":"topMentionedLimit","prettyName":"Number of top mentioned users","type": "integer",
                    "default": 10}]

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(TopMentioned, cls).get_args()

    @classmethod
    def get_type(cls):
        return cls.__type_name

    ####################################################################################################################

    @classmethod
    def get(cls, analytics_meta):

        gridfs, db_col, args, schema_id = cls.setup(analytics_meta)

        mention_limit = args["topMentionedLimit"]
        data = cls.get_top_mentioned(schema_id, mention_limit, db_col)
        result = {"details": {"chartType": "bar"}, "data": data}
        cls.export_json(analytics_meta, json.dumps(result), gridfs)

        return True


    @classmethod
    def get_top_mentioned(cls, schema_id, limit, db_col):

        cls._logger.info("Attempting to get top mentioned users")

        mention_key = Status.SCHEMA_MAP[schema_id]["mentions"]
        user_id_key = mention_key + "." + UserMention.SCHEMA_MAP[schema_id]["id"]
        user_name_key = mention_key + "." + UserMention.SCHEMA_MAP[schema_id]["name"]

        top_user_query = [
            {"$unwind": "$" + mention_key},
            {"$group": {"_id": '$' + user_name_key, "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": limit}]

        top_users = db_col.aggregate(top_user_query, allowDiskUse=True)

        return list(top_users)