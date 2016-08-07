import logging

import networkx as nx

from AnalysisEngine.Graphing.Trends.HashtagTrend import HashtagTrend
from AnalysisEngine.Graphing.Trends.TrendGraph import TrendGraph
from AnalyticsService import Util
from AnalyticsService.TwitterObj import Status, User
from AnalysisEngine.Classification.ClassificationSystem import ClassificationSystem

class HashtagTrendReweet2(TrendGraph):
    _logger = logging.getLogger(__name__)
    __arguments = [dict(name="userLimit", prettyName="Number of users", type="integer", default=1000),
                   dict(name="hashtag_grouping", prettyName="Hashtag Groupings", type="dictionary_list", variable=False,
                        default=[
                            dict(name="Leave",
                                 tags=["no2eu", "notoeu", "betteroffout", "voteout", "eureform", "britainout",
                                       "leaveeu", "voteleave", "beleave", "loveeuropeleaveeu"], color=None),
                            dict(name="Remain",
                                 tags=["yes2eu", "yestoeu", "betteroffin", "votein", "ukineu", "bremain",
                                       "strongerin", "leadnotleave", "voteremain"], color=None)])]

    _node_color = ("type", {"source": "red", "target": "lime", "TimeIndicator": "purple"})
    _edges_color = ("type", {"retweet": "gold", "user": "steelblue"})

    def __init__(self, analytics_meta):
        super(HashtagTrendReweet2, self).__init__(analytics_meta)

    @classmethod
    def get_type(cls):
        return "Hashtag User Trend Retweet 2 Graph"

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(HashtagTrendReweet2, cls).get_args()

    def get_color(self):
        return self._node_color, self._edges_color

    def process(self):

        time_interval = self.args["timeInterval"]
        limit = self.args["Limit"]
        top_user_limit = self.args["userLimit"]
        hashtag_args = self.args["hashtag_grouping"]

        class_labels = {hashtag_args[0]["name"]: -1, hashtag_args[1]["name"]: 1}
        hashtag_groupings = dict([(i, -1) for i in hashtag_args[0]["tags"]] +
                                 [(i, 1) for i in hashtag_args[1]["tags"]])
        classification_system = ClassificationSystem("BASIC", class_labels, hashtag_groupings)

        user_ids = HashtagTrend.get_top_users(self.schema, top_user_limit, self.col)

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

            date = status.get_created_at()
            end_date = date
            time_step = self.get_time_step(date, start_date, time_interval)
            max_time_step = time_step
            status_id = str(status.get_id())

            source_user = status.get_user()
            source_id = str(source_user.get_id())

            current_score, _ = classification_system.consume(status)
            user = status.get_user()
            source_user_id = user.get_id()
            source_node_id = str(source_user_id) + ":" + str(status_id)

            G.add_node(source_node_id,
                           label="usr:" + user.get_name(),
                           tweet=status.get_text().replace("\n", " "),
                           type="source",
                           node_type="user",
                           username=user.get_name(),
                           date=str(date),
                           gravity_x=float(time_step),
                           gravity_y=float(current_score),
                           gravity_x_strength=float(10),
                           gravity_y_strength=float(10))

            self.link_node_to_history(G, history, source_node_id, source_user_id)

            retweet = status.get_retweet_status()
            if retweet is not None:
                user = retweet.get_user()
                user_id = user.get_id()
                target_node_id = str(user_id) + ":" + str(status_id)
                # Ignore the vain people retweeting themselves
                if user_id != source_id:
                    G.add_node(target_node_id,
                                   label="usr:" + user.get_name(),
                                   type="target",
                                   node_type="user",
                                   username=user.get_name(),
                                   tweet=status.get_text().replace("\n", " "),
                                   date=str(date),
                                   gravity_x=float(time_step),
                                   gravity_y=float(0.0),
                                   gravity_x_strength=float(10),
                                   gravity_y_strength=float(0.001))

                    self.link_node_to_history(G, history, target_node_id, user_id)
                    G.add_edge(source_node_id, target_node_id, type="retweet")

        return G, start_date
