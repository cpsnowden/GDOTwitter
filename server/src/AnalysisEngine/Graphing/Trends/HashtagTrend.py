import logging

import networkx as nx

from AnalysisEngine.Graphing.Trends.TrendGraph import TrendGraph
from AnalyticsService import Util
from AnalysisEngine.Classification.ClassificationSystem import ClassificationSystem
from AnalyticsService.TwitterObj import Status, User


class HashtagTrend(TrendGraph):
    _logger = logging.getLogger(__name__)
    __type_name = "Hashtag User Trend Graph"
    __arguments = [dict(name="userLimit", prettyName="Number of users", type="integer", default=1000),
                   {'name': "hashtag_grouping", 'prettyName': "Hashtag Groupings", 'type': "dictionary_list",
                    'variable': False, 'default': [
                       dict(name="Leave", tags=["no2eu", "notoeu", "betteroffout", "voteout", "eureform", "britainout",
                                                "leaveeu", "voteleave", "beleave", "loveeuropeleaveeu"], color=None),
                       dict(name="Remain", tags=["yes2eu", "yestoeu", "betteroffin", "votein", "ukineu", "bremain",
                                                 "strongerin", "leadnotleave", "voteremain"], color=None)]}
                   ]

    _node_color = ("type", dict(status="blue", source="red", target="lime"))
    _edges_color = ("type", dict(source="gold", target="turquoise"))

    def __init__(self, analytics_meta):
        super(HashtagTrend, self).__init__(analytics_meta)

    @classmethod
    def get_type(cls):
        return "Hashtag Graph"

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(HashtagTrend, cls).get_args()

    def get_color(self):
        return self._node_color, self._edges_color

    def process(self):

        time_interval = self.args["timeInterval"]
        limit = self.args["Limit"]
        top_user_limit = self.args["userLimit"]
        hashtag_args = self.args["hashtag_grouping"]

        class_labels = {hashtag_args[0]["name"]: -1, hashtag_args[1]["name"]: 1}
        hashtag_groupings = dict([(i,-1) for i in hashtag_args[0]["tags"]] +
                                 [(i, 1) for i in hashtag_args[1]["tags"]])
        classification_system = ClassificationSystem("BASIC", class_labels, hashtag_groupings)


        user_ids = self.get_top_users(self.schema, top_user_limit, self.col)

        query = self.get_time_bounded_query({Util.join_keys(Status.SCHEMA_MAP[self.schema]["user"],
                                                            User.SCHEMA_MAP[self.schema]["id"]): {"$in": user_ids}})
        cursor = self.get_sorted_cursor(query, limit)

        if cursor is None:
            self.analytics_meta.status = "NO DATA IN RANGE"
            self.analytics_meta.save()
            return False

        G, start_date = self.build_graph(cursor, time_interval, classification_system)

        self._logger.info("Build graph %s", self.analytics_meta.id)
        self.analytics_meta.status = "BUILT"
        self.analytics_meta.save()

        G = self.layout(G)
        G = self.add_time_indicator_nodes(G, start_date)
        self.finalise_graph(G, self.get_color())

        return True

    def build_graph(self, cursor, time_interval, classification_system):

        G = nx.DiGraph()

        history = {}

        start_date = Status(cursor[0], self.schema).get_created_at()

        for status_json in cursor:
            status = Status(status_json, self.schema)

            time_step = self.get_time_step(status.get_created_at(), start_date, time_interval)

            status_id = str(status.get_id())
            current_score, _ = classification_system.consume(status)

            self.add_user_node(G, status, time_step, status_id, "source", history, current_score)

        return G, start_date

    def add_user_node(self, G, status, time_step, status_id, node_type, history, score):
        user = status.get_user()
        user_id = user.get_id()
        node_id = str(user_id) + ":" + str(status_id)

        G.add_node(node_id,
                   label="usr:" + user.get_name() + ":" + status.get_text().replace("\n", " "),
                   type=node_type,
                   node_type = "user",
                   username = user.get_name(),
                   tweet = status.get_text().replace("\n", " "),
                   date=str(status.get_created_at()),
                   gravity_x=float(time_step),
                   gravity_y=float(score),
                   gravity_x_strength=float(10),
                   gravity_y_strength=float(10))

        self.link_node_to_history(G, history, node_id, user_id)

    @staticmethod
    def get_top_users(schema, limit, col):

        user_id_key = Util.dollar_join_keys(Status.SCHEMA_MAP[schema]["user"],
                                            User.SCHEMA_MAP[schema]["id"])

        query = [
            {"$group": {"_id": {'id': user_id_key}, "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": limit}
        ]

        return [user["_id"]["id"] for user in col.aggregate(query, allowDiskUse=True)]
