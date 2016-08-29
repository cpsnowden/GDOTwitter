import logging

import networkx as nx

from AnalysisEngine import Util
from AnalysisEngine.Classification.CommunityUser.CommunityUser import CommunityUser
from AnalysisEngine.Graphing.Graphing import Graphing
from AnalysisEngine.Graphing.Utils.GraphUtils import color_names
from AnalysisEngine.TwitterObj import Status
from AnalysisEngine.TwitterObj import User


class RetweetCommunityClassificationUser(Graphing):
    _logger = logging.getLogger(__name__)
    __arguments = [dict(name="retweet", prettyName="Retweet Edges", type="boolean",
                        default=True),
                   dict(name="mention", prettyName="Mention Edges", type="boolean",
                        default=True),
                   dict(name="hashtag_grouping", prettyName="Hashtag Groupings", type="dictionary_list", variable=False,
                        default=[
                            dict(name="Leave",
                                 tags=["no2eu", "notoeu", "betteroffout", "voteout", "eureform", "britainout",
                                       "leaveeu", "voteleave", "beleave", "loveeuropeleaveeu"],
                                 color=dict(color="crimson", options=color_names)),
                            dict(name="Remain", tags=["yes2eu", "yestoeu", "betteroffin", "votein", "ukineu", "red",
                                                      "strongerin", "leadnotleave", "voteremain"],
                                 color=dict(color="darkviolet", options=color_names))]),
                   dict(name="include_tweet_text", prettyName="Include Tweet Text", type="boolean",
                        default=False),
                   dict(name="only_include_top_users", prettyName="Only include top user nodes", type="boolean",
                        default=False),
                   dict(name="UserLimit", prettyName="User limit", type="integer",
                        default=20000),
                   dict(name="get_max_component", prettyName="Max component", type="boolean",
                        default=True)]

    _edges_color = ("type", dict(retweet="powderblue", mention="gold", both="lightsage"))
    _node_color = ("type", dict(retweeted="powderblue", retweeter="lime", both="blueviolet"))

    def __init__(self, analytics_meta):
        super(RetweetCommunityClassificationUser, self).__init__(analytics_meta)

    @classmethod
    def get_type(cls):
        return "Top User Retweet Graph with Classification"

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(RetweetCommunityClassificationUser, cls).get_args()

    def get_color(self):
        return self._node_color, self._edges_color

    def get_top_users(self, limit):

        user_name_key = Util.dollar_join_keys(Status.SCHEMA_MAP[self.schema]["user"],
                                              User.SCHEMA_MAP[self.schema]["name"])

        query = [{"$group": {"_id": user_name_key, "count": {"$sum": 1}}},
                 {"$sort": {"count": -1}},
                 {"$limit": limit}]

        cursor = list(self.col.aggregate(query, allowDiskUse=True))
        return set([i["_id"] for i in cursor])

    def process(self):

        limit = self.args["Limit"]
        include_mention_edges = self.args["mention"]
        include_retweet_edges = self.args["retweet"]
        only_include_top_users = self.args["only_include_top_users"]
        include_text = self.args["include_tweet_text"]
        get_max = self.args["get_max_component"]
        hashtag_scores = dict([(i["name"], i["tags"]) for i in self.args["hashtag_grouping"]])
        node_colors = ("classification", dict([(i["name"], i["color"]["color"]) for i in self.args[
            "hashtag_grouping"]]))

        self._logger.info("Got the following tags dictionary: %s", hashtag_scores)
        self._logger.info("Using color labelling: %s", node_colors)
        self._logger.info("Include mention edges: %s", include_mention_edges)
        self._logger.info("Include retweet edges: %s", include_retweet_edges)

        user_name_key = Util.join_keys(Status.SCHEMA_MAP[self.schema]["user"],
                                       User.SCHEMA_MAP[self.schema]["name"])

        user_query = {}
        top_users = None
        if self.args["UserLimit"] > 0:
            self._logger.info("Getting top users")
            top_users = self.get_top_users(self.args["UserLimit"])
            user_query = {user_name_key: {"$in": list(top_users)}}
            self._logger.info("Got top users")
        query = self.get_time_bounded_query(user_query)

        cursor = self.get_sorted_cursor(query, limit)
        if cursor is None:
            self.analytics_meta.status = "NO DATA IN RANGE"
            self.analytics_meta.save()
            return False

        G, users = self.build_graph(cursor, include_retweet_edges, include_mention_edges, hashtag_scores,
                                    include_text, only_include_top_users, get_max, top_users)
        G = self.assign_classifications(G, users)

        self._logger.info("Build graph %s", self.analytics_meta.id)
        self.analytics_meta.status = "BUILT"
        self.analytics_meta.save()

        self._logger.info("Exported community data %s", self.analytics_meta.id)

        G = self.layout(G)
        self.finalise_graph(G, (node_colors, self._edges_color))

        return True

    def build_graph(self, cursor, include_retweet_edges, include_mention_edges, hashtag_scores, include_text,
                    only_include_top_users, get_max, top_users=None):

        G = nx.DiGraph()
        users = {}

        for status_json in cursor:

            status = Status(status_json, self.schema)

            # Add the source user
            source_user = status.get_user()
            source_user_id = str(source_user.get_name())

            if source_user_id not in users:
                users[source_user_id] = CommunityUser(classification_scores=hashtag_scores)

                G.add_node(source_user_id, username=source_user.get_name(),
                           node_type="user")

            if include_text:
                if "tweet" not in G.node[source_user_id]:
                    G.node[source_user_id]["tweet"] = "|" + status.get_text().replace("\n", "") + "|"
                else:
                    G.node[source_user_id]["tweet"] += "|" + status.get_text().replace("\n", "") + "|"

            source_user_obj = users[source_user_id]
            source_user_obj.said(status)

            G.node[source_user_id]["no_statuses"] = source_user_obj.get_number_statuses()

            retweet = status.get_retweet_status()
            if include_retweet_edges and retweet is not None:
                retweeted_user = retweet.get_user(True)
                retweeted_user_id = str(retweeted_user.get_name())
                if not(only_include_top_users and top_users is not None and retweeted_user_id not in top_users):
                    if retweeted_user_id not in users:
                        users[retweeted_user_id] = CommunityUser(classification_scores=hashtag_scores)
                        G.add_node(retweeted_user_id, username=retweeted_user.get_name(), node_type="user")

                    user_obj = users[retweeted_user_id]
                    user_obj.retweeted_by(source_user_obj)
                    user_obj.said(retweet)
                    G.node[retweeted_user_id]["no_statuses"] = user_obj.get_number_statuses()
                    G.node[retweeted_user_id]["no_times_retweeted"] = user_obj.number_of_times_retweets

                    if not G.has_edge(source_user_id, retweeted_user_id):
                        G.add_edge(source_user_id, retweeted_user_id, type="retweet", number_tweets=1)
                    else:
                        G[source_user_id][retweeted_user_id]["number_tweets"] += 1
                        if G[source_user_id][retweeted_user_id]["type"] == "mention":
                            G[source_user_id][retweeted_user_id]["type"] = "both"

            elif include_mention_edges:
                for mention in status.get_mentions():
                    mentioned_user_id = str(mention.get_name())
                    if only_include_top_users and top_users is not None and mentioned_user_id not in top_users:
                        continue

                    if mentioned_user_id not in users:
                        users[mentioned_user_id] = CommunityUser(classification_scores=hashtag_scores)
                        G.add_node(mentioned_user_id, username=mention.get_name(), node_type="user")

                    user_obj = users[mentioned_user_id]
                    user_obj.mentioned()
                    G.node[mentioned_user_id]["no_times_mentioned"] = user_obj.number_of_times_mentioned

                    if not G.has_edge(source_user_id, mentioned_user_id):
                        G.add_edge(source_user_id, mentioned_user_id, type="mention", number_tweets=1)
                    else:
                        G[source_user_id][mentioned_user_id]["number_tweets"] += 1
                        if G[source_user_id][mentioned_user_id]["type"] == "retweet":
                            G[source_user_id][mentioned_user_id]["type"] = "both"
        if get_max:
            return max(nx.strongly_connected_component_subgraphs(G), key=len), users
        else:
            return G, users

    def assign_classifications(self, graph, users):
        for node in graph.nodes():
            graph.node[node]["classification"] = users[node].get_classification()
        return graph
