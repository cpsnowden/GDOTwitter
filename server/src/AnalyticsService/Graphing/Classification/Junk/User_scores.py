import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
from xml.etree import ElementTree
import sys
from xml.etree import ElementTree

# with open("/Users/ChrisSnowden/Downloads/A_Brexitold_4d5.graphml","rb") as f:
#     tree = ElementTree.parse(f)
#
#

# reload(sys)
# sys.setdefaultencoding('utf-8')
score = []
G = nx.read_graphml("/Users/ChrisSnowden/Downloads/A_Brexitold_2a5.graphml")
for nid, attrs in G.nodes(data=True):
    # print nid, attrs
    if "user_score" in attrs:
        score.append(attrs["user_score"])

n, bins, patches = plt.hist(score, 50, normed=1, facecolor='green', alpha=0.75)

plt.show()
# import random
# G=nx.Graph()
#
# for i in xrange(10):
#     G.add_node(i, test_attr=str(random.random()) + "_attr")
# nx.write_graphml(G, "test.graphml")
# #
#
# ns = {"graphml": "http://graphml.graphdrawing.org/xmlns"}
#
# with open("test.graphml") as f:
#     tree = ElementTree.parse(f)
# keys = {}
# for key_entry in tree.findall("{http://graphml.graphdrawing.org/xmlns}key"):
#     print key_entry.attrib['attr.name'], key_entry.attrib['id']
#     keys[key_entry.attrib['id']] = key_entry.attrib['attr.name']
#     key_entry.attrib['id'] = key_entry.attrib['attr.name']
#     print key_entry.attrib['attr.name'], key_entry.attrib['id']
# root = tree.find("graphml:graph", ns)
#
# for data_entry in root.iter("{http://graphml.graphdrawing.org/xmlns}data"):
#     # print data_entry.attrib['key']
#     found_key = data_entry.attrib['key']
#     data_entry.set('key',keys[found_key])
#     # print data_entry.attrib['key']
#
# # print ElementTree.tostring(tree, encoding='utf8', method='xml')
# ElementTree.register_namespace('',ns.values()[0])
# tree.write("output.graphml",encoding='utf8', method='xml')
# # ,default_namespace=ns.values()[0])