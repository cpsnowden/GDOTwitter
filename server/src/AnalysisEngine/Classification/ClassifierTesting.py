from TweetClassifier.Basic import Basic
import re
import csv
from sklearn import metrics

leave = "leave",
leave_tags = ["no2eu", "notoeu", "betteroffout", "voteout", "eureform", "britainout",
              "leaveeu", "voteleave", "beleave", "loveeuropeleaveeu"]
remain = "remain"
remain_tags = ["yes2eu", "yestoeu", "betteroffin", "votein", "ukineu", "red",
               "strongerin", "leadnotleave", "voteremain"]

basic = Basic(None, dict([(i,1) for i in leave_tags] + [(i,-1) for i in remain_tags]))

mapping = {1:"leave",-1:"remain",0:"unknown"}
reverse_mappings = {"leave":1,"remain":-1,"unknown":0}

path = "Training/labelling_text_BREXIT.dat"

data = csv.reader(open(path, 'rb'), delimiter=',', quotechar='|')

class Demo:

    def __init__(self, text):
        self.text = text
    def get_hashtags(self):
        return re.findall(r"#(\w+)", self.text)

true_labels = []
found_labels = []
for row in data:
    # if row[0] == "unknown":
    #     continue

    result = basic.predict(Demo(row[1]))
    s = result.confidence * result.classification

    if s > 0:
        l = "leave"
    elif s < 0:
        l = "remain"
    else:
        l="unknown"

    true_labels.append(reverse_mappings[row[0]])
    found_labels.append(s)


print metrics.classification_report(true_labels, found_labels, labels = [-1,1,0],
                                    target_names=["remain","leave","unknown"])