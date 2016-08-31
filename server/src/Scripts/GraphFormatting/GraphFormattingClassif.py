import os
import sys
from xml.etree import ElementTree

import networkx as nx

from AnalysisEngine.Graphing.Utils.GraphUtils import GraphColor


def fix_graphml_format_better(name, out):

    replacements = {}
    with open(name) as f:
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

    with open(out, "w") as des:
        tree.write(des, encoding='utf-8', method='xml')

# _node_color = ("type", {"source": "red", "target": "lime", "TimeIndicator": "purple"})
_edges_color = ("type", {"retweet": "gold", "user": "steelblue"})

# _edges_color = ("type", dict(retweet="blue", mention="gold", both="red"))
# _node_color = ("type", dict(retweeted="red", retweeter="lime", both="blueviolet"))

# _edges_color = ("type", dict(retweet="powderblue", mention="gold", both="lightsage"))
_node_color = ("node_type", dict(Leave="crimson", Remain="darkgreen",TimeIndicator="purple"))

path = sys.argv[1]
print "Input Path", path


G = nx.read_graphml(path)

for nid in G.nodes():
    node = G.node[nid]
    try:
        node["size"] = 3
        t = node["type"]
        if t == "source":
            if node["user_score"] < 0:
                node["node_type"] = "Leave"
                print "Processing Leave"
            elif node["user_score"] > 0:
                node["node_type"] = "Remain"
                print "Processing Remain"
            else:
                node["node_type"] = "Unknown"
                print "Processing Unknown"
        elif t == "target":
            node["node_type"] = "Retweeted"
            print "Processing Retweeted"
        else:
            node["node_type"] = t
            print "Processing " + t
    except KeyError:
        print "AAAHHH", node

print "Coloring"
GraphColor.color_graph(G, (_node_color,_edges_color))


prefix = os.path.splitext(path)[0]
temp_path =  prefix + "_temp.graphml"

print "Output temp"
nx.write_graphml(G, temp_path)


print "Fixing"
fix_graphml_format_better(temp_path, prefix + "_fmt.graphml")