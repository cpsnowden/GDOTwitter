import matplotlib.pyplot as plt
import csv
import numpy as np

def get_date(path):
    traction = []
    swing = []
    with open(path) as f:
        reader = csv.reader(f)
        i = 0
        for row in reader:
            i +=1
            if i == 1:
                continue
            traction.append(float(row[0]))
            swing.append(float(row[1]))
    plt.subplot(211)
    plt.plot(swing, label = "swing:" + path)
    plt.plot(traction, label = "tract:" + path)
    plt.subplot(212)
    plt.plot(np.array(swing) / np.array(traction))

    return traction, swing


get_date("Storage.dat")
get_date("Storage_nl.dat")
plt.subplot(211)
plt.legend()
plt.show()
#
# import networkx as nx
# import random
# from xml.etree import ElementTree
# nNodes = 1000
# nEdges = 500
# G = nx.gnm_random_graph(nNodes, nEdges)
#
#
# path = "with_gravity_x_1000_500_nl"
# nx.write_graphml(G,path+".graphml")
#
# replacements = {}
# with open(path + ".graphml")as f:
#     tree = ElementTree.parse(f)
#
#     for key_entry in tree.findall("{http://graphml.graphdrawing.org/xmlns}key"):
#         key_name = key_entry.attrib['attr.name']
#         id = key_entry.attrib['id']
#         key_entry.attrib['id'] = key_name
#         replacements[id] = key_name
#     root = tree.getroot()
#     for data_entry in root.iter("{http://graphml.graphdrawing.org/xmlns}data"):
#         found_key = data_entry.attrib['key']
#         data_entry.set('key', replacements[found_key])
#
#     ElementTree.register_namespace('', "http://graphml.graphdrawing.org/xmlns")
#
# with open(path + "_fmt.graphml","w") as des:
#     tree.write(des, encoding='utf-8', method='xml')
#
#
# for n in G.nodes():
#     G.node[n]["gravity_x"] =  random.triangular(-2.0, 2.0)
#     G.node[n]["gravity_y"] =  random.triangular(-2.0, 2.0)
#
# path = "with_gravity_x_1000_500"
# nx.write_graphml(G,path+".graphml")
#
# replacements = {}
# with open(path + ".graphml")as f:
#     tree = ElementTree.parse(f)
#
#     for key_entry in tree.findall("{http://graphml.graphdrawing.org/xmlns}key"):
#         key_name = key_entry.attrib['attr.name']
#         id = key_entry.attrib['id']
#         key_entry.attrib['id'] = key_name
#         replacements[id] = key_name
#     root = tree.getroot()
#     for data_entry in root.iter("{http://graphml.graphdrawing.org/xmlns}data"):
#         found_key = data_entry.attrib['key']
#         data_entry.set('key', replacements[found_key])
#
#     ElementTree.register_namespace('', "http://graphml.graphdrawing.org/xmlns")
#
# with open(path + "_fmt.graphml","w") as des:
#     tree.write(des, encoding='utf-8', method='xml')
