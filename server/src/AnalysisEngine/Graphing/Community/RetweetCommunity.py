import json
import logging
from collections import Counter
from itertools import product

import community
import networkx as nx

from AnalysisEngine.Classification.CommunityUser.CommunityUser import CommunityUser
from AnalysisEngine.Graphing.Graphing import Graphing
from AnalysisEngine.TwitterObj import Status
from AnalysisEngine.Graphing.Utils.GraphUtils import color_names

class RetweetCommunity(Graphing):
    _logger = logging.getLogger(__name__)
    __arguments = [dict(name="resolution", prettyName="Community Detection Resolution", type="integer",
                        default=1.0),
                   dict(name="fractionToClassify", prettyName="Fraction of nodes to classify", type="integer",
                        default=0.05),
                   dict(name="retweet", prettyName="Retweet Edges", type="boolean",
                        default=True),
                   dict(name="mention", prettyName="Mention Edges", type="boolean",
                        default=True),
                   dict(name="hashtag_grouping", prettyName="Hashtag Groupings", type="dictionary_list", variable=True,
                        default=[
                            dict(name="Trump", tags=["makeamericagreatagain", "trump2016"],
                                 color=dict(color = "darkgreen", options=color_names)),
                            dict(name="Saunders", tags=["feelthebern"],
                                 color=dict(color = "darkviolet", options=color_names)),
                            dict(name="Clinton", tags=["imwithher"],
                                 color=dict(color="crimson", options=color_names))])]

    _edges_color = ("type", dict(retweet="blue", mention="gold", both="red"))
    _node_color = ("type", dict(retweeted="red", retweeter="lime", both="blueviolet"))

    def __init__(self, analytics_meta):
        super(RetweetCommunity, self).__init__(analytics_meta)

    @classmethod
    def get_type(cls):
        return "Retweet Community Graph"

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(RetweetCommunity, cls).get_args()

    def get_color(self):
        return self._node_color, self._edges_color

    def process(self):

        limit = self.args["Limit"]
        resolution = self.args["resolution"]
        include_mention_edges = self.args["mention"]
        include_retweet_edges = self.args["retweet"]
        fraction = self.args['fractionToClassify']

        hashtag_scores = dict([(i["name"], i["tags"]) for i in self.args["hashtag_grouping"]])
        node_colors = ("classification", dict([(i["name"], i["color"]["color"]) for i in self.args[
            "hashtag_grouping"]]))

        self._logger.info("Got the following tags dictionary: %s", hashtag_scores)
        self._logger.info("Include mention edges: %s", include_mention_edges)
        self._logger.info("Include retweet edges: %s", include_retweet_edges)

        query = self.get_time_bounded_query({})
        cursor = self.get_sorted_cursor(query, limit)
        if cursor is None:
            self.analytics_meta.status = "NO DATA IN RANGE"
            self.analytics_meta.save()
            return False

        G, users = self.build_graph(cursor, include_retweet_edges, include_mention_edges, hashtag_scores)
        G = self.detect_communities(G, users, resolution, fraction)

        self._logger.info("Build graph %s", self.analytics_meta.id)
        self.analytics_meta.status = "BUILT"
        self.analytics_meta.save()

        self.export_json(self.analyse_inter_community(G, hashtag_scores))
        self._logger.info("Exported community data %s", self.analytics_meta.id)

        G = self.layout(G)
        self.finalise_graph(G, (node_colors, self._edges_color))

        return True

    def build_graph(self, cursor, include_retweet_edges, include_mention_edges, hashtag_scores):

        G = nx.DiGraph()
        users = {}

        for status_json in cursor:

            status = Status(status_json, self.schema)

            # Add the source user
            source_user = status.get_user()
            source_user_id = str(source_user.get_name())

            if source_user_id not in users:
                users[source_user_id] = CommunityUser(classification_scores=hashtag_scores)
                G.add_node(source_user_id, username = source_user.get_name(),
                           node_type="user")

            source_user_obj = users[source_user_id]
            source_user_obj.said(status)

            G.node[source_user_id]["no_statuses"] = source_user_obj.get_number_statuses()

            retweet = status.get_retweet_status()
            if include_retweet_edges and retweet is not None:
                retweeted_user = retweet.get_user(True)
                retweeted_user_id = str(retweeted_user.get_name())

                if retweeted_user_id not in users:
                    users[retweeted_user_id] = CommunityUser(classification_scores=hashtag_scores)
                    G.add_node(retweeted_user_id, username = retweeted_user.get_name(), node_type="user")

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

        return max(nx.connected_component_subgraphs(G.to_undirected()), key=len), users

    def detect_communities(self, graph, users, resolution, fraction):

        partitions = community.best_partition(graph.to_undirected(), resolution=resolution)

        counter = Counter(partitions.values())
        number_of_nodes = sum(counter.values())

        self._logger.info("Counter %s", counter)

        communities = [i for i in counter.items() if i[1] > fraction * number_of_nodes]

        self._logger.info("Number of nodes: %d", number_of_nodes)
        self._logger.info("Number of communities to map: %d", len(communities))
        self._logger.info("Communities: %s", communities)

        partitions_to_com = dict.fromkeys(set(partitions.values()), CommunityUser.UNCLASSIFIED)

        output = {}

        for com, _ in communities:
            com_nodes = [users[n].get_classification() for n in partitions.keys() if partitions[n] == com]
            com_classes = Counter(com_nodes)

            self._logger.info("%d: %s", com, com_classes)
            partitions_to_com[com] = com_classes.most_common(1)[0][0]
            output[com] = (partitions_to_com[com], com_classes)

        for node in graph.nodes():
            c = partitions[node]
            graph.node[node]["community"] = c
            graph.node[node]["classification"] = partitions_to_com[c]

        # json.dump(output, open("per_classification.txt", "w"))

        return graph

    def analyse_inter_community(self, G, hashtag_scores):

        community_labels = hashtag_scores.keys() + [CommunityUser.UNCLASSIFIED]
        community_size = dict.fromkeys(community_labels, 0.0)
        for node, d in G.nodes(data=True):
            classification = d["classification"]
            community_size[classification] += 1.0

        return {"community_size": community_size,
               "retweet_connection": self.analyse_edge_type(G, "retweet", community_labels,
                                                            community_size),
               "mention_connection": self.analyse_edge_type(G, "mention", community_labels,
                                                            community_size),
               "both_connection": self.analyse_edge_type(G, "both", community_labels,
                                                         community_size)}


    def analyse_edge_type(self, G, edge_type, community_labels, community_size):

        self._logger.info("Analysing edge type: %s", edge_type)
        community_interconnection = product(community_labels, community_labels)
        community_interconnection_size = dict.fromkeys(community_interconnection, 0.0)
        for u, v, d in G.edges_iter(data=True):
            if d["type"] != edge_type:
                continue
            source_node_cls = G.node[u]["classification"]
            target_node_cls = G.node[v]["classification"]
            community_interconnection_size[(source_node_cls, target_node_cls)] += d["number_tweets"]

        community_interconnection_density = dict.fromkeys(community_interconnection, 0.0)

        for (s, t) in community_interconnection_size.keys():
            if community_size[s] == 0 or community_size[t] == 0:
                normaliser = 1.0
            else:
                normaliser = float(community_size[s] * community_size[t])
            community_interconnection_density[(s, t)] = community_interconnection_size[(s, t)] / normaliser

        return {"inter_size": community_interconnection_size,
                "inter_density": community_interconnection_density}
