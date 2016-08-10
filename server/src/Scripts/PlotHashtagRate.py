from dateutil import parser
from collections import OrderedDict
# import matplotlib.pyplot as plt
import json
# import mpld3
# import matplotlib.dates as md
dpi = 1

tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]
for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)

path =  "/Users/ChrisSnowden/IndividualProject/GDOTwitter/DATA/RAW_A_TwitterBre_64.json"
with open(path) as f:
    data = json.load(f)


data = data["data"]

x_categories = [parser.parse(i) for i in data["categories"]]
y_labels = OrderedDict.fromkeys(x_categories, 0)

# fig = plt.figure(figsize=(1920 / dpi, 1080 / dpi), dpi=dpi, )
# fig,ax = plt.subplots()


for i,series in enumerate(data["values"]):
    for entry in series["data"]:
        y_labels[parser.parse(entry["dt"])] = entry["count"]
    # l = ax.plot(x_categories, list(y_labels.values()), label=series["_id"], color = tableau20[i])
    if series["_id"] == "voteleave":
        leave = y_labels
        break
    if series["_id"] != "voteleave":
        continue
    # elif series["_id"]=="voteremain":
    #     remain = y_labels
    # elif series["_id"] == "brexit":
    #     brexit = y_labels
    y_labels = OrderedDict.fromkeys(x_categories, 0)

# # ax[1].plot(x_categories,)
# xfmt = md.DateFormatter('%Y-%m-%d\n %H:%M:%S')
#
# ax.xaxis.set_major_formatter(xfmt)
# plt.legend()
#
# fig,axs = plt.subplots(nrows=2)
# axs[0].plot(x_categories, brexit.values())
# axs[1].plot(x_categories, remain.values())
# axs[1].plot(x_categories, leave.values())
# axs[1].xaxis.set_major_formatter(xfmt)


import networkx as nx


G = nx.Graph()
import datetime
(datetime.datetime.now() - datetime.datetime.now()).total_seconds() / 60

first = True
for i,t_step in enumerate(leave):
    if first:
        start = t_step

    time_step = float((t_step-start).total_seconds()) / 60
    print start, t_step, time_step

    G.add_node(i, x=float(time_step), y = float(leave[t_step]),
               date = str(t_step), gravity_x = float(time_step),
               gravity_y = float(leave[t_step]), size = 0.5, label = "")
    if not first:
        G.add_edge(i-1,i)

    last = t_step
    first = False


f = True
for j in xrange(0, int((last-start).total_seconds()), 60*60*24):
    time = start + datetime.timedelta(seconds=j)
    print "Time Node", time
    G.add_node("t:" + str(j), label = str(time),
               x=float(j)/60, y = float(-50), gravity_x = float(j)/60, gravity_y = float(-50), size = 5)
    if not f:
        G.add_edge("t:"+str(j-1),"t:" + str(j))

    f = False


nx.write_graphml(G, "/Users/ChrisSnowden/IndividualProject/GDOTwitter/DATA/leave_rate_gravity" + ".graphml")

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


fix("/Users/ChrisSnowden/IndividualProject/GDOTwitter/DATA/leave_rate_gravity")
#
# import numpy as np
#
# # # plt.figure()
# # fig,ax = plt.subplots()
# # ratios = []
# # for i in x_categories:
# #     ratio = float(leave[i]) / brexit[i]
# #     #
# #     # ratio = float(leave[i]) - remain[i]
# #     ratios.append(ratio)
# #
# # plt.plot(x_categories, ratios)
# # ratios = []
# # for i in x_categories:
# #     ratio = float(remain[i]) / brexit[i]
# #     #
# #     # ratio = float(leave[i]) - remain[i]
# #     ratios.append(ratio)
# # plt.plot(x_categories, ratios)
# # xfmt = md.DateFormatter('%Y-%m-%d\n %H:%M:%S')
# #
#
# #
# # # mpld3.save_html(fig, f)
# # # plt.close("all")
# # plt.show()