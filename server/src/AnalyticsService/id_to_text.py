from pymongo import MongoClient
import csv
from AnalyticsService.TwitterObj import Status
import sys
reload(sys)  # just to be sure
sys.setdefaultencoding('utf-8')


db_col = MongoClient().get_database("DATA").get_collection("Brexit_old")

id_lab = {}
with open("labelling_out_BREXIT.dat") as f:
    reader = csv.reader(f)
    for row in reader:
        id_lab[long(row[1])] = row[0]
# print id_lab.keys()
cursor = db_col.find({"id": {"$in":id_lab.keys()}})
print cursor.count()

with open("labelling_text_BREXIT.dat","w") as out:
    writer = csv.writer(out, delimiter=",", quotechar="|", quoting=csv.QUOTE_ALL)
    for c in cursor:
        s = Status(c, "T4J")
        writer.writerow([id_lab[s.get_id()],s.get_text().replace("\n"," ")])
        # print s.get_id()