from pymongo import MongoClient

from AnalyticsService.TwitterObj import Status
import json
import numpy as np

if False:
    schema_id = "RAW"
    db_col = MongoClient().get_database("DATA").get_collection("Trump_Clinton_Saunders_old")
    trump = "trump_old"
    top_hashtag_file = "top_hashtags_" + trump + ".dat"
    coocurrences_file = "coocurences_" + trump + ".npy"
    indices_file = "indices_" + trump + ".json"
    graph = "g_" + trump + ".graphml"

else:
    schema_id = "T4J"
    db_col = MongoClient().get_database("DATA").get_collection("Brexit_old")
    brexit = "brexit_old"
    top_hashtag_file = "top_hashtags_" + brexit + ".dat"
    coocurrences_file = "coocurences_" + brexit + ".npy"
    indices_file = "indices_" + brexit + ".json"
    graph = "g_" + brexit + ".graphml"


if False:
    limit = 2000

    hashtag_key = Status.SCHEMA_MAP[schema_id]["hashtags"]
    top_user_query = [
        {"$match": {Status.SCHEMA_MAP[schema_id]["retweeted_status"]: {"$exists": False}, "lang": "en"}},
        {"$unwind": "$" + hashtag_key},
        {"$group": {"_id": {"$toLower": '$' + hashtag_key + '.' + 'text'}, "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": limit}]

    top_hastags = db_col.aggregate(top_user_query, allowDiskUse=True)
    a = list(top_hastags)
    print a

    with open(top_hashtag_file, "w") as f:
        json.dump(a, f)
elif False:
    top_hasthag_count = json.load(open(top_hashtag_file))
    top_hasthag_count = sorted(top_hasthag_count, key=lambda x: x["count"], reverse=True)
    top_hashtags = set([i["_id"] for i in top_hasthag_count if i["_id"]])
    # not in ["ivoted", "brexit"]])
    print top_hasthag_count
    print top_hashtags

    n = len(top_hashtags)
    coocurences_array = np.zeros([n,n], dtype=int)
    import itertools
    import pprint
    coocurrences = dict.fromkeys(itertools.combinations(top_hashtags,2), 0)
    indices = dict(zip(top_hashtags,range(len(top_hashtags))))
    pprint.pprint(indices)
    cursor = db_col.find({Status.SCHEMA_MAP[schema_id]["retweeted_status"]: {"$exists": False}, "lang": "en"})
    ids = []
    n = 0
    for c in cursor:
        s = Status(c, schema_id)
        # id = str(s.get_retweet_status().get_id())
        # if len(ids) > 50000:
        #     break
        # if id in ids:
        #     # print "Ignoring duplicate"
        #     continue
        # else:
        #     ids.append(id)
        n+=1

        htags = [i.lower() for i in s.get_hashtags()]
        thtags = list(set(htags) & top_hashtags)
        if not (2 < len(thtags) <= 3):
            continue
        print n, thtags
        for h1 in thtags:
            for h2 in thtags:
                if h1 != h2:
                    if (h1,h2) in coocurrences:
                        coocurrences[(h1, h2)] += 1
                    else:
                        coocurrences[(h2, h1)] += 1

    for i,j in coocurrences.keys():
        i_index = indices[i]
        j_index = indices[j]
        value = coocurrences[(i,j)]
        coocurences_array[i_index,j_index] = value
        coocurences_array[j_index,i_index] = value

    np.save(coocurrences_file, coocurences_array,)
    with open(indices_file,"w") as f:
        json.dump(indices, f)


    import operator
    sorted_x = sorted(coocurrences.items(), key=operator.itemgetter(1), reverse=True)
    print sorted_x[:10]

else:
    d  = np.load(coocurrences_file).astype(float)
    ids = json.load(open(indices_file))
    ri = dict([(i1, i2) for (i2, i1) in ids.items()])

    row_sum = d.sum(axis=1)
    col_sum = d.sum(axis=0)
    # print d
    idx_cols = col_sum.argsort()[::-1]
    idx_rows = row_sum.argsort()[::-1]
    # print idx_cols,idx_rows
    d = d[:, idx_cols][idx_rows, :][:2000,:2000]
    # print d.shape
    # print d
    # exit()
    row_sum = d.sum(axis=1, keepdims=True)
    col_sum = d.sum(axis=0, keepdims=True)
    score = d / (row_sum + col_sum - d)
    score[~ np.isfinite(score)] = 0
    score *= 10
    # print score.shape
    # me= score.mean()
    score[score < score.mean() + score.std() * 3.0] = 0.0
    # print score.mean()
    import networkx as nx
    #
    # print score
    G = nx.Graph(score)
    G = max(nx.connected_component_subgraphs(G.to_undirected()), key=len)
    labels = []
    for nid in G.nodes():
        labels.append(ri[idx_cols[nid]])
        G.node[nid]["label"] = ri[idx_cols[nid]]
    nx.write_graphml(G, graph)
    np.save("score_large", score)
    adjMatrix =  nx.adjacency_matrix(G)
    # np.savetxt("foo.csv", d, delimiter=",")


    from sklearn.cluster import spectral_clustering

    clstr =  spectral_clustering(adjMatrix, n_clusters=3)
    import pprint
    pprint.pprint(zip(labels,clstr))
