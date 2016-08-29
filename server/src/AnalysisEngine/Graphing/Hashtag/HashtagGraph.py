import logging

import networkx as nx
import numpy as np

from AnalysisEngine.Graphing.Graphing import Graphing
from AnalysisEngine.TwitterObj import Status

class HashtagGraph(Graphing):
    _logger = logging.getLogger(__name__)
    __arguments = [dict(name="hashtag_limit", prettyName="Number of hashtags", type="integer",
                        default=250),
                   dict(name="filter_max_component", prettyName="Filter max component", type="boolean",
                        default=True)]

    _edges_color = ("type", {"colocation": "gold"})
    _node_color = ("type", {"hashtag": "blue"})

    def __init__(self, analytics_meta):
        super(HashtagGraph, self).__init__(analytics_meta)

    @classmethod
    def get_type(cls):
        return "Hashtag Occurences Graph"

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(HashtagGraph, cls).get_args()

    def get_color(self):
        return self._node_color, self._edges_color

    def process(self):
        limit = self.args["hashtag_limit"]
        filter_component = self.args["filter_max_component"]
        self._logger.info("Getting the top hashtags")
        top_hashtags = self.get_top_non_retweeted_hashtags(self.col, limit, self.schema)
        self._logger.info("Got " + str(len(top_hashtags)) + " top hashtags")
        print top_hashtags
        G = self.build_graph(filter_component, top_hashtags)

        self._logger.info("Build graph %s", self.analytics_meta.id)
        self.analytics_meta.status = "BUILT"
        self.analytics_meta.save()

        G = self.layout(G, {"EDGE_WEIGHT_INFLUENCE": 3.0})
        self.finalise_graph(G)
        return True

    def build_graph(self, filter_component, top_hashtags):
        G = nx.Graph()

        n = len(top_hashtags)
        coocurences_array = np.zeros([n, n], dtype=int)
        top_hashtags_to_id = dict(zip(top_hashtags, range(len(top_hashtags))))
        for i, h in enumerate(top_hashtags):
            G.add_node(i, label=h, type="hashtag")

        cursor = self.col.find({"$or": [{Status.SCHEMA_MAP[self.schema]["retweeted_status_exists"]: {"$exists": False}},
                                        {Status.SCHEMA_MAP[self.schema]["retweeted_status_exists"]: {"$eq": None}}]})

        for i,c in enumerate(cursor):
            s = Status(c, self.schema)

            f_htags = set([i.lower() for i in s.get_hashtags()])
            htags = f_htags & top_hashtags

            for h1 in htags:
                h1_index = top_hashtags_to_id[h1]
                coocurences_array[h1_index][h1_index] += 1
                for h2 in htags:
                    if h1 != h2:
                        h2_index = top_hashtags_to_id[h2]
                        coocurences_array[h1_index][h2_index] += 1
                        coocurences_array[h2_index][h1_index] += 1
        print coocurences_array
        row_sum = coocurences_array.sum(axis=1, keepdims=True)
        col_sum = coocurences_array.sum(axis=0, keepdims=True)
        score = coocurences_array.astype(float) / (row_sum + col_sum - coocurences_array)
        score[~ np.isfinite(score)] = 0
        np.fill_diagonal(score, 0.0)
        upper95 = score.mean() + 3 * score.std()
        score *= 3.0 / upper95

        min_occurences = min(row_sum)[0]
        max_occurences = max(row_sum)[0]

        for i, h in enumerate(top_hashtags):
            G.node[i]["n_occurences"] = float(row_sum[i][0])
            G.node[i]["size"] = 2 + 40 * (float(row_sum[i][0]) - min_occurences) / (max_occurences - min_occurences)

        for row in xrange(0, n):
            for col in xrange(row + 1, n):
                if score[row][col] != 0:
                    G.add_edge(row, col, weight=float(score[row][col]), type="colocation")
        if filter_component:
            G = max(nx.connected_component_subgraphs(G), key=len)
        return G

    @staticmethod
    def get_top_non_retweeted_hashtags(db_col, limit, schema_id):

        hashtag_key = Status.SCHEMA_MAP[schema_id]["hashtags"]
        top_hashtag_query = [
            {"$match": {"$or":[{Status.SCHEMA_MAP[schema_id]["retweeted_status_exists"]:{"$exists": False}},
                               {Status.SCHEMA_MAP[schema_id]["retweeted_status_exists"]:{"$eq": None}}]}},
            {"$unwind": "$" + hashtag_key},
            {"$group": {"_id": {"$toLower": '$' + hashtag_key + '.' + 'text'}, "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": limit}]

        cursor = db_col.aggregate(top_hashtag_query, allowDiskUse=True)

        top_hashtags = set([i["_id"] for i in cursor])

        return top_hashtags
