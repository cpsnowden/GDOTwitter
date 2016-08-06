import logging

import networkx as nx

from AnalysisEngine.Graphing.Graphing import Graphing
from AnalyticsService.TwitterObj import Status

class BasicRetweet(Graphing):
    _logger = logging.getLogger(__name__)
    __arguments = [dict(name="filter_max_component", prettyName="Filter max component", type="boolean", default=True)]

    _edges_color = ("type", dict(retweet="blue"))
    _node_color = ("type", dict(retweeted="red", retweeter="lime", both="blueviolet"))

    def __init__(self, analytics_meta):
        super(BasicRetweet, self).__init__(analytics_meta)


    @classmethod
    def get_type(cls):
        return "Basic Retweet Graph"

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(BasicRetweet, cls).get_args()

    def get_color(self):
        return self._node_color, self._edges_color

    def process(self):

        limit = self.args["Limit"]
        filter_component = self.args["filter_max_component"]

        query = self.get_time_bounded_query({Status.SCHEMA_MAP[self.schema]["retweeted_status"]: {"$exists": True,
                                                                                                  "$ne": None}})
        cursor = self.get_sorted_cursor(query, limit)
        if cursor is None:
            self.analytics_meta.status = "NO DATA IN RANGE"
            self.analytics_meta.save()
            return False

        G = self.build_graph(cursor, filter_component)

        self._logger.info("Build graph %s", self.analytics_meta.id)
        self.analytics_meta.status = "BUILT"
        self.analytics_meta.save()

        G = self.layout(G)
        self.finalise_graph(G)

    def build_graph(self, cursor, filter_component):

        G = nx.DiGraph()
        retweeters = set()
        retweeted = set()

        for status_json in cursor:

            status = Status(status_json, self.schema)

            # Add the source user
            source_user = status.get_user()
            source_user_id = str(source_user.get_id())

            if source_user_id not in retweeted and source_user_id not in retweeters:
                G.add_node(source_user_id,
                               label=source_user.get_name(),
                               type="retweeter")

            retweeters.add(source_user_id)

            if source_user_id in retweeted:
                G.node[source_user_id]["type"] = "both"

            target_user = status.get_retweet_status().get_user()
            target_user_id = str(target_user.get_id())

            if target_user_id not in retweeted and target_user_id not in retweeters:
                G.add_node(target_user_id,
                               label=target_user.get_name(),
                               type="retweeted")

            if target_user_id in retweeters:
                G.node[target_user_id]["type"] = "both"

            retweeted.add(target_user_id)

            G.add_edge(source_user_id, target_user_id, type="retweet", tweet=status.get_text())

        if filter_component:
            G = max(nx.connected_component_subgraphs(G), key=len)

        return G