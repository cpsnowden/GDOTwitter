import networkx as nx
import untangle
import random
import string
import os
import time
import numpy as np
from xml.etree import ElementTree

def old_fix_xml(inp, outp):
    obj = untangle.parse(inp)
    replace = []
    replacements = {}
    # Replaces ids such as "d10" to actual attributes, ex "size"
    for key in obj.graphml.key:
        name = '"' + key['attr.name'] + '"'
        key_id = '"' + key['id'] + '"'
        name.replace(" ", "")

        replacements[key_id] = name
        replace.append(key_id)

    lines = []
    with open(inp) as infile:
        #For strict ordering
        for line in infile:
            for src in replace:
                line = line.replace(src, replacements[src])
            lines.append(line)
    with open(outp, 'w') as outfile:
        for line in lines:
            outfile.write(line)

def new_fix_xml(inp, outp):

    replacements = {}
    with open(inp) as f:
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

    with open(outp, "w") as des:
        tree.write(des, encoding='utf-8', method='xml')


def createRandomGraph(nNodes, nEdges, path):
    attribute_keys = string.ascii_lowercase[:6]
    attribute_keys2 = string.ascii_lowercase[6:10]
    G = nx.gnm_random_graph(nNodes, nEdges)
    for n in G.nodes():
        for k in attribute_keys:
            G.node[n][k] =  random.randint(0, 5000)
        for k in attribute_keys2:
            G.node[n][k] = "blah"
    for u,v in G.edges():
        for k in attribute_keys:
            G[u][v][k] = random.randint(0, 5000)

    nx.write_graphml(G, path)

def create_graphs(_range):
    for i in _range:
        n_nodes = i
        n_edges = n_nodes * 2

        createRandomGraph(n_nodes, n_edges, str(n_nodes) + "_" + str(n_edges) + ".graphml")
        print n_nodes

def test_path(path, n = 1):
    results = []
    for n in xrange(n):
        results.append(test_instance(path))

    new = [i[0] for i in results]
    # old = [i[1] for i in results]
    old = [i[1] for i in results]
    print "Results new:", np.mean(new), "old:", np.mean(old)
    return new, old

def test_instance(path):
    if random.random() <= 0.5:
        new = test_new(path)
        # old = test_old(path)
        old = 0
    else:
        # old = test_old(path)
        old = 0
        new = test_new(path)

    return new,old

def test_old(path):
    out_path = os.path.splitext(path)[0] + "_temp.graphml"
    start = time.time()
    old_fix_xml(path, out_path)
    old = time.time() - start
    print path, "old", old
    return old

def test_new(path):
    out_path = os.path.splitext(path)[0] + "_temp.graphml"
    start = time.time()
    new_fix_xml(path, out_path)
    new = time.time() - start
    print path, "new", new
    os.remove(out_path)
    return new

def test(range):
    results = []
    import json
    with open("test_results.dat","w") as f:
        for i in range:
            n_nodes = i
            n_edges = n_nodes * 2

            new, old = test_path(str(n_nodes) + "_" + str(n_edges) + ".graphml", 2)
            results = {"nodes": n_nodes, "edges": n_edges, "newT": new, "oldT": old}
            f.write(json.dumps(results )+ "\n")
        return results

# test_path("100_50.graphml",2)
# create_graphs(xrange(200000,1000000,100000))
test(xrange(400000,1000000,100000))
# create_graphs()
# createRandomGraph(100,50,"100_50.graphml")