import logging

import networkx as nx

from AnalysisEngine import Util
from AnalysisEngine.Graphing.Trends.TrendGraph import TrendGraph
from AnalysisEngine.Graphing.Utils.GraphUtils import color_names
from AnalysisEngine.TwitterObj import Status, User, UserMention


class MultiUserRelationship(TrendGraph):
    _logger = logging.getLogger(__name__)
    __arguments = [dict(name="users", prettyName="Users", type="dictionary_list", variable=True,
                        default=[
                            dict(name="FederalBritain", tags=[],
                                 color=dict(color="darkgreen", options=color_names)),
                            dict(name="RickPoleway", tags=[],
                                 color=dict(color="darkviolet", options=color_names)),
                            dict(name="NickStevenson63", tags=[],
                                 color=dict(color="crimson", options=color_names)),
                            dict(name="mjs64", tags=[],
                                 color=dict(color="lime", options=color_names))])]

    _node_color = ("type", {"source": "red", "target": "lime", "TimeIndicator": "purple"})
    _edges_color = ("type", {"retweet": "powderblue", "user": "sienna", "mention": "gold", "authored": "grey"})

    def __init__(self, analytics_meta):
        super(MultiUserRelationship, self).__init__(analytics_meta)

    @classmethod
    def get_type(cls):
        return "Multi User Relationship"

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(MultiUserRelationship, cls).get_args()

    def get_color(self):
        return self._node_color, self._edges_color

    def process(self):

        time_interval = self.args["timeInterval"]

        user_name_key = Util.join_keys(Status.SCHEMA_MAP[self.schema]["user"],
                                       User.SCHEMA_MAP[self.schema]["name"])
        mention_key = Util.join_keys(Status.SCHEMA_MAP[self.schema]["mentions"],
                                     UserMention.SCHEMA_MAP[self.schema]["name"])
        retweet_user_key = Util.join_keys(Status.SCHEMA_MAP[self.schema]["retweeted_status"],
                                          Status.SCHEMA_MAP[self.schema]["retweet_user"],
                                          User.SCHEMA_MAP[self.schema]["retweet_screen_name"])

        node_colors = ("type", dict([("user:" + i["name"], i["color"]["color"]) for i in self.args["users"]]))
        user_names = [i["name"] for i in self.args["users"]]

        query = self.get_time_bounded_query({user_name_key: {"$in": user_names},
                                             "$or": [
                                                 {mention_key: {"$in": user_names}},
                                                 {retweet_user_key: {"$in": user_names}}
                                             ]})

        self._logger.info("Query %s" ,query)

        cursor = self.get_sorted_cursor(query)
        if cursor is None:
            self.analytics_meta.status = "NO DATA IN RANGE"
            self.analytics_meta.save()
            return False

        G, start_date = self.build_graph(cursor, time_interval, user_names)

        self._logger.info("Build graph %s", self.analytics_meta.id)
        self.analytics_meta.status = "BUILT"
        self.analytics_meta.save()

        G = self.layout(G)
        # G = self.add_time_indicator_nodes(G, start_date)

        self.finalise_graph(G, (node_colors, self._edges_color))

        return True

    def build_graph(self, cursor, time_interval, users):

        G = nx.DiGraph()

        history = {}

        start_date = Status(cursor[0], self.schema).get_created_at()

        for status_json in cursor:
            status = Status(status_json, self.schema)

            date = status.get_created_at()
            time_step = self.get_time_step(date, start_date, time_interval)
            status_id = str(status.get_id())

            user = status.get_user()
            source_user_id = user.get_name()
            source_node_id = str(source_user_id) + ":" + str(status_id)

            G.add_node(source_node_id,
                       label="usr:" + user.get_name(),
                       type="user:" + user.get_name(),
                       tweet=status.get_text().replace("\n", " "),
                       username=user.get_name(),
                       node_type="user",
                       date=str(date),
                       gravity_x=float(time_step),
                       gravity_x_strength=float(1))

            self.link_node_to_history(G, history, source_node_id, source_user_id)

            retweet = status.get_retweet_status()
            if retweet is not None:
                user = retweet.get_user(True)
                retweeted_user_id = user.get_name()
                if retweeted_user_id in users:
                    target_node_id = str(retweeted_user_id) + ":" + str(status_id)
                    # Ignore the vain people retweeting themselves
                    if retweeted_user_id != source_user_id:
                        G.add_node(target_node_id,
                                   label="usr:" + user.get_name(),
                                   type="user:" + retweeted_user_id,
                                   node_type="user",
                                   username=user.get_name(),
                                   gravity_x=float(time_step),
                                   gravity_x_strength=float(1))

                        self.link_node_to_history(G, history, target_node_id, retweeted_user_id)
                        G.add_edge(source_node_id, target_node_id, type="retweet")
            else:
                for mention in status.get_mentions():
                    mentioned_user_id = str(mention.get_name())
                    if mentioned_user_id not in users and mentioned_user_id:
                        continue

                    target_node_id = str(mentioned_user_id) + ":" + str(status_id)
                    G.add_node(target_node_id,
                               label="usr:" + mentioned_user_id,
                               type="user:" + mentioned_user_id,
                               node_type="user",
                               username=mentioned_user_id,
                               gravity_x=float(time_step),
                               gravity_x_strength=float(1))

                    self.link_node_to_history(G, history, target_node_id, mentioned_user_id)
                    G.add_edge(source_node_id, target_node_id, type="mention")

        return G, start_date
