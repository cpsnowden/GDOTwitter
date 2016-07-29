import logging

import networkx as nx
import numpy as np

from AnalyticsService.Graphing.Graph import Graph
from AnalyticsService.TwitterObj import Status


class HashtagCollocationGraph(Graph):
    _logger = logging.getLogger(__name__)

    __type_name = "Hashtag Collocation Graph"
    __arguments = [{"name": "limit", "prettyName": "Number of hashtags", "type": "integer",
                    "default": 250},
                   {"name": "filter_max_component", "prettyName": "Filter max component", "type": "boolean",
                    "default": True}]

    _edges_color = ("type", {"colocation": "gold"})
    _node_color = ("type", {"hashtag": "blue"})

    @classmethod
    def get_color(cls):
        return cls._node_color, cls._edges_color

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(HashtagCollocationGraph, cls).get_args()

    @classmethod
    def get_type(cls):
        return cls.__type_name

    ####################################################################################################################

    @classmethod
    def get(cls, analytics_meta):

        gridfs, db_col, args, schema_id = cls.setup(analytics_meta)

        limit = args["limit"]
        filter_component = args["filter_max_component"]

        top_hashtags = cls.get_top_non_retweeted_hashtags(db_col, limit, schema_id)

        n = len(top_hashtags)
        coocurences_array = np.zeros([n, n], dtype=int)
        top_hashtags_to_id = dict(zip(top_hashtags, range(len(top_hashtags))))

        G = nx.Graph()
        for i, h in enumerate(top_hashtags):
            G.add_node(i, label=h, type = "hashtag")
        cls._logger.info("Getting collocation")
        cursor = db_col.find({Status.SCHEMA_MAP[schema_id]["retweeted_status"]: {"$exists": False}, "lang": "en"})

        for c in cursor:
            s = Status(c, schema_id)

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

        row_sum = coocurences_array.sum(axis=1, keepdims=True)
        col_sum = coocurences_array.sum(axis=0, keepdims=True)

        score = coocurences_array.astype(float) / (row_sum + col_sum - coocurences_array)
        score[~ np.isfinite(score)] = 0
        np.fill_diagonal(score, 0.0)

        upper95 = score.mean() + 3 * score.std()
        # score *= 3.0 / score.max()
        score *= 3.0 / upper95
        cls._logger.info("Adding graph edges")
        for row in xrange(0, n):
            for col in xrange(row + 1, n):
                if score[row][col] != 0:
                    G.add_edge(row, col, weight=float(score[row][col]), type = "colocation")

        if filter_component:
            G = max(nx.connected_component_subgraphs(G), key=len)

        G = cls.layout(G, analytics_meta, gridfs, args, {"EDGE_WEIGHT_INFLUENCE": 3.0})
        cls.finalise_graph(G, gridfs, analytics_meta, cls.get_color())

        return True

    @classmethod
    def get_top_non_retweeted_hashtags(cls, db_col, limit, schema_id):
        cls._logger.info("Getting top hashtags")
        hashtag_key = Status.SCHEMA_MAP[schema_id]["hashtags"]
        top_hashtag_query = [
            {"$match": {Status.SCHEMA_MAP[schema_id]["retweeted_status"]: {"$exists": False}, "lang": "en"}},
            {"$unwind": "$" + hashtag_key},
            {"$group": {"_id": {"$toLower": '$' + hashtag_key + '.' + 'text'}, "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": limit}]

        cursor = db_col.aggregate(top_hashtag_query, allowDiskUse=True)

        top_hashtags = set([i["_id"] for i in cursor])

        return top_hashtags
