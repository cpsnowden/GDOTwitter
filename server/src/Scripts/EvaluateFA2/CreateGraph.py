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

    intra_community_distance = {}
    for c in inv_map:
        intra_community_distance[c] = get_inter_nodes_distance(G, inv_map[c])
        inter_community_distance = {}

    for c1, c2 in combinations(inv_map.keys(), 2):
        inter_community_distance[(c1, c2)] = get_intra_community_distance(G,
                                                                          inv_map[c1],
                                                                          inv_map[c2])

    inter_node_ratios = {}
    for c1, c2 in inter_community_distance:
        inter_node_ratios[(c1, c2)] = np.power(inter_community_distance[(c1, c2)], 2) / (
            intra_community_distance[c1] * intra_community_distance[c2]
        )

    pprint.pprint(intra_community_distance)
    pprint.pprint(inter_community_distance)

    # pprint.pprint(inter_node_ratios)

    return np.average(inter_node_ratios.values()), np.std(inter_node_ratios.values())


def get_intra_community_distance(G, c1, c2):
    distance = 0
    n = 0
    for n1 in c1:
        for n2 in c2:
            distance += get_distance(G.node[n1], G.node[n2])
            n += 1
    return float(distance) / n


def get_inter_nodes_distance(G, nodes):
    distance = 0
    n = 0
    for n1, n2 in combinations(nodes, 2):
        distance += get_distance(G.node[n1], G.node[n2])
        n += 1
    return float(distance) / n


def get_distance(n1, n2):
    return np.sqrt(np.power(n1["x"] - n2["x"], 2) + np.power(n1["y"] - n2["y"], 2))


print testGraph("large_test_oo.graphml")
print testGraph("large_test_fa2.graphml")
