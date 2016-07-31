import networkx as nx
import community

G = nx.read_graphml("good_use_election_partition.graphml")


for nid in G.nodes():
    print nid, G.node[nid]


partition_dict = community.best_partition(G, resolution=1)
print partition_dict


partitions = set(partition_dict.values())
hashtag_sets = dict((i,[]) for i in partitions)

for entry in partition_dict:
    G.node[entry]["paritition"] = partition_dict[entry]
    hashtag_sets[partition_dict[entry]].append(G.node[entry]["label"])

import pprint
pprint.pprint(hashtag_sets)

nx.write_graphml(G, "parititioned_us_hashtags")
#
# from sklearn.cluster import spectral_clustering
# clstr =  spectral_clustering(nx.to_numpy_matrix(G), n_clusters=8)

import pprint
# print clstr
# pprint.pprint(zip(labels,clstr))

