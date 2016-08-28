from pymongo import MongoClient
import json
import networkx as nx
from collections import Counter
from AnalysisEngine.TwitterObj import Status
from AnalysisEngine.Classification.CommunityUser.CommunityUser import CommunityUser
import community

wrongs = []
def detect_communities(graph, users, resolution=1.0, fraction=0.05):
    partitions = community.best_partition(graph.to_undirected(), resolution=resolution)

    counter = Counter(partitions.values())
    number_of_nodes = sum(counter.values())
    communities = [i for i in counter.items() if i[1] > fraction * number_of_nodes]

    partitions_to_com = dict.fromkeys(set(partitions.values()), CommunityUser.UNCLASSIFIED)

    output = {}

    for com, _ in communities:
        com_nodes = [users[n].get_classification() for n in partitions.keys() if partitions[n] == com]
        com_classes = Counter(com_nodes)
        partitions_to_com[com] = com_classes.most_common(1)[0][0]
        output[com] = (partitions_to_com[com], com_classes)

    for node in graph.nodes():
        c = partitions[node]
        graph.node[node]["community"] = c
        graph.node[node]["classification"] = partitions_to_com[c]
        if partitions_to_com[c] != "Unclassified" and users[node].get_classification() != "Unclassified":
            if partitions_to_com[c] != users[node].get_classification():
                print node, partitions_to_com[c], users[node].get_classification()
                wrongs.append({"user":node,"louvian": partitions_to_com[c], "class": users[node].get_classification()})
    return graph



client = MongoClient()
db = client.get_database("DATA")
auth = db.authenticate("twitterApplication", "gdotwitter", source="admin")
col = db.get_collection("Trump_Clinton_Saunders_old")

hashtags = dict(name="hashtag_grouping", prettyName="Hashtag Groupings", type="dictionary_list", variable=True,
                default=[
                    dict(name="Trump", tags=["makeamericagreatagain", "trump2016"], color="blue"),
                    dict(name="Saunders", tags=["feelthebern"], color="lime"),
                    dict(name="Clinton", tags=["imwithher"], color="red")])



hashtag_scores = dict([(i["name"], i["tags"]) for i in hashtags["default"]])

users = {}
G = nx.DiGraph()
cursor = col.find()

for status_json in cursor:

    status = Status(status_json, "RAW")

    # Add the source user
    source_user = status.get_user()
    source_user_id = str(source_user.get_name())

    if source_user_id not in users:
        users[source_user_id] = CommunityUser(classification_scores=hashtag_scores)
        G.add_node(source_user_id, username=source_user.get_name(),
                   node_type="user")

    source_user_obj = users[source_user_id]
    source_user_obj.said(status)

    G.node[source_user_id]["no_statuses"] = source_user_obj.get_number_statuses()

    retweet = status.get_retweet_status()
    if  retweet is not None:
        retweeted_user = retweet.get_user(True)
        retweeted_user_id = str(retweeted_user.get_name())

        if retweeted_user_id not in users:
            users[retweeted_user_id] = CommunityUser(classification_scores=hashtag_scores)
            G.add_node(retweeted_user_id, username=retweeted_user.get_name(), node_type="user")

        user_obj = users[retweeted_user_id]
        user_obj.retweeted_by(source_user_obj)
        user_obj.said(retweet)
        G.node[retweeted_user_id]["no_statuses"] = user_obj.get_number_statuses()
        G.node[retweeted_user_id]["no_times_retweeted"] = user_obj.number_of_times_retweets

        if not G.has_edge(source_user_id, retweeted_user_id):
            G.add_edge(source_user_id, retweeted_user_id, type="retweet", number_tweets=1)
        else:
            G[source_user_id][retweeted_user_id]["number_tweets"] += 1

principle = max(nx.connected_component_subgraphs(G.to_undirected()), key=len)

G = detect_communities(G, users)

json.dump(wrongs, open("WrongUsers.json","w"))