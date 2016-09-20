import networkx as nx
import random
from itertools import combinations
import community
import numpy as np
import pprint
import random
from itertools import combinations
G = nx.Graph()

def createGraph(N, out, p = 2):
    G = nx.Graph()
    for x in xrange(N):
        G.add_node(x)

    pairs = list(combinations(G.nodes(),2))

    chosen = random.sample(pairs, N*p)

    for n1,n2 in chosen:
        G.add_edge(n1,n2)
    #
    # for n1 in G.nodes():
    #     for n2 in G.nodes():
    #         if n1 != n2 and random.random() < p:
    #             G.add_edge(n1, n2)
    print out
    nx.write_graphml(G, out)




# createGraph(0.1, 1000, "TEST_1000.graphml")

createGraph(1000, "TEST_1000.graphml")
# createGraph(5000, "TEST_5000.graphml")
# createGraph(10000, "TEST_10000.graphml")
# createGraph(25000, "TEST_25000.graphml")
# createGraph(50000, "TEST_50000.graphml")