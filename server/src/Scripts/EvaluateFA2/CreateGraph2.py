import networkx as nx
import random
from itertools import combinations
import community
import numpy as np
import pprint

G = nx.Graph()


def createCluster(p, start, end):
    G = nx.Graph()
    for x in xrange(start, end):
        G.add_node(x)

    for n1 in G.nodes():
        for n2 in G.nodes():
            if n1 != n2 and random.random() < p:
                G.add_edge(n1, n2)
    return G


def createGraph(p, q, n, N):
    G = nx.Graph()
    sub_graphs = []
    for i in xrange(N):
        H = createCluster(p, i * n, i * n + n)
        sub_graphs.append(H)
        G = nx.compose(G, H)

    for sub1, sub2 in combinations(sub_graphs, 2):
        for n1 in sub1:
            for n2 in sub2:
                if random.random() < q:
                    G.add_edge(n1, n2)

    return G


def createTestGraph(p, q, n, N):
    G = createGraph(p, q, n, N)
    nx.write_graphml(G, "test_" + str(p) + "_" + str(q) + "_" + str(n) + "_" + str(N) + ".graphml")


# createTestGraph(0.1, 0.005, 100, 5)
# print G
# nx.draw_networkx(G)


# plt.show()

def testGraph(fileName, r=1):
    G = nx.read_graphml(fileName)
    partitions = community.best_partition(G, resolution=r)

    inv_map = {}
    for k, v in partitions.iteritems():
        inv_map[v] = inv_map.get(v, [])
        inv_map[v].append(k)

    community_centroids = {}
    for k in inv_map:
        community_centroids[k] = get_centroid(G, inv_map[k])

    community_ditances = {}
    for c1,c2 in combinations(community_centroids,2):
        community_ditances[(c1,c2)] = get_distance(community_centroids[c1],
                                                   community_centroids[c2])

    print np.average(community_ditances.values())
    print get_graph_distance(G)


def get_graph_distance(G):

    min_x = None
    min_y = None
    max_x = None
    max_y = None
    first = True
    for n in G.nodes():
        node = G.node[n]
        x = node["x"]
        y = node["y"]
        if first:
            min_x = x
            max_x = x
            min_y = y
            max_y = y
            first = False
        else:
            if x < min_x:
                min_x = x
            if x > max_x:
                max_x = x
            if y < min_y:
                min_y = y
            if y > max_y:
                max_y = y

    return get_distance_points(min_x,min_y, max_x, max_y)

def get_distance_points(x1,x2,y1,y2):
    return np.sqrt(np.power(x1 - x2, 2) + np.power(y1 - y2, 2))

def get_centroid(G, nodes):

    x = []
    y = []
    for n in nodes:
        x.append(G.node[n]["x"])
        y.append(G.node[n]["y"])

    return np.mean(x), np.mean(x)

def get_distance(n1, n2):
    return np.sqrt(np.power(n1[0] - n2[0], 2) + np.power(n1[1] - n2[1], 2))


# testGraph("test_fa2.graphml")
# testGraph("test_oo.graphml")

testGraph("large_test_fa2.graphml")
print "Open Ord"
testGraph("large_test_oo.graphml")