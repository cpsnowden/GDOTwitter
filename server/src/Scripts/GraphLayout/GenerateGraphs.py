import networkx as nx
import random
from xml.etree import ElementTree


def fix(path):
    replacements = {}
    with open(path + ".graphml")as f:
        tree = ElementTree.parse(f)

        for key_entry in tree.findall("{http://graphml.graphdrawing.org/xmlns}key"):
            key_name = key_entry.attrib['attr.name']
            id = key_entry.attrib['id']
            key_entry.attrib['id'] = key_name
            replacements[id] = key_name
        root = tree.getroot()
        for data_entry in root.iter("{http://graphml.graphdrawing.org/xmlns}data"):
            found_key = data_entry.attrib['key']
            data_entry.set('key', replacements[found_key])

        ElementTree.register_namespace('', "http://graphml.graphdrawing.org/xmlns")

    with open(path + "_fmt.graphml","w") as des:
        tree.write(des, encoding='utf-8', method='xml')

# nNodes = 10000
# nEdges = 5000
# G = nx.gnm_random_graph(nNodes, nEdges)
#
# for n in G.nodes():
#     G.node[n]["x"] =  random.uniform(-100.0, 100.0)
#     G.node[n]["y"] =  random.uniform(-100.0, 100.0)
#
# path = "with_gravity_x_" + str(nNodes) + "_" + str(nEdges)
# nx.write_graphml(G,path+".graphml")
# fix(path)
#
# for n in G.nodes():
#     G.node[n]["gravity_x"] =  random.triangular(-2.0, 2.0)
#     G.node[n]["gravity_y"] =  random.triangular(-2.0, 2.0)
#
# path = "with_gravity_x_" + str(nNodes) + "_" + str(nEdges) + "with_cogs"
# nx.write_graphml(G,path+".graphml")
# fix(path)


G = nx.Graph()

G.add_path(list(xrange(0,100)) + [0])

for u,v in G.edges():
    print u,v

for n in G.nodes():
    G.node[n]["x"] =  random.uniform(-100.0, 100.0)
    G.node[n]["y"] =  random.uniform(-100.0, 100.0)

path = "circle_nocog"
nx.write_graphml(G, path + ".graphml")
fix(path)

for n in G.nodes():
    G.node[n]["gravity_x"] =  random.uniform(-5.0, 5.0)
    G.node[n]["gravity_y"] =  random.uniform(-5.0, 5.0)

path = "circle_cog"
nx.write_graphml(G, path + ".graphml")
fix(path)
