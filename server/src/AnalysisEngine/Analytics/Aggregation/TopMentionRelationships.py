import logging

from AnalysisEngine import Util
from AnalysisEngine.Analytics.Analytics import Analytics
from AnalysisEngine.TwitterObj import Status, User, UserMention


class TopMentionRelationships(Analytics):
    _logger = logging.getLogger(__name__)
    __arguments = [dict(name="Limit", prettyName="Number of top relationships users", type="integer",
                        default=10)]

    def __init__(self, analytics_meta):
        super(TopMentionRelationships, self).__init__(analytics_meta)

    @classmethod
    def get_type(cls):
        return "Top BiLateral Mention Relationships"

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(TopMentionRelationships, cls).get_args()

    def process(self):
        limit = self.args["Limit"]

        user_name_key = Util.dollar_join_keys(Status.SCHEMA_MAP[self.schema]["user"],
                                              User.SCHEMA_MAP[self.schema]["name"])

        mention_key = Util.join_keys(Util.dollar_join_keys(Status.SCHEMA_MAP[self.schema]["mentions"]),
                                       UserMention.SCHEMA_MAP[self.schema]["name"])

        query = [
            {"$match": self.time_bound_aggr()},
            {"$match": {"$or": [{Status.SCHEMA_MAP[self.schema]["retweeted_status_exists"]: {"$exists": False}},
                                {Status.SCHEMA_MAP[self.schema]["retweeted_status_exists"]: {"$eq": None}}]}},
            {"$unwind": Util.dollar_join_keys(Status.SCHEMA_MAP[self.schema]["mentions"])},
            {"$project": {
                "_id": 1,
                "AB": {"$cond": [{"$gt": [mention_key, user_name_key]},
                                 1,
                                 0]},
                "BA": {"$cond": [{"$lte": [mention_key, user_name_key]},
                                 1,
                                 0]},
                "groupId": {"$cond": [{"$gt": [mention_key, user_name_key]},
                                      {"A": mention_key, "B":user_name_key},
                                      {"A": user_name_key, "B": mention_key}]}}
            },
            {"$group": {"_id": "$groupId", "count": {"$sum": 1}, "AB": {"$sum": "$AB"}, "BA": {"$sum": "$BA"}}},
            {"$project": {
                "_id": 1,
                "count": 1,
                "AB": 1,
                "BA": 1,
                "Metric": {"$abs": {"$divide": [{"$multiply": ["$AB", "$BA"]}, {"$add": ["$AB", "$BA"]}]}}
            }},
            {"$sort": {"Metric": -1}},
            {"$limit": limit}
        ]

        data = list(self.col.aggregate(query, allowDiskUse=True))

        for i in data:
            userA = list(self.col.find({Util.join_keys(Status.SCHEMA_MAP[self.schema]["user"],
                                                 User.SCHEMA_MAP[self.schema]["name"]):i["_id"]["A"]}).limit(1))
            if len(userA) > 0:
                i["A_pic"] = Status(userA[0],self.schema).get_user(False).get_image_url().replace("_normal","")
            else:
                i["A_pic"] = ""

            userB = self.col.find({Util.join_keys(Status.SCHEMA_MAP[self.schema]["user"],
                                                  User.SCHEMA_MAP[self.schema]["name"]): i["_id"]["B"]}).limit(1)

            if len(userA) > 0:
                i["B_pic"] = Status(userB[0], self.schema).get_user(False).get_image_url().replace("_normal", "")
            else:
                i["B_pic"] = ""

        self.export_html(result=data,
                         properties={"chartProperties": {"yAxisName": "Number of Mentions",
                                                         "xAxisName": "User Pair (A<->B)",
                                                         "caption": self.dataset_meta.description,
                                                         "subcaption": "Top " + str(limit) + " mentioning relationships"},
                                     "analysisType": "pair_ranking",
                                     "chartType": "stackedbar2d"},
                         export_type="chart")
        self.export_json(data)
        return True