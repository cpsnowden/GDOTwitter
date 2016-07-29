from pymongo import MongoClient
from TwitterObj import Status
import csv
import progressbar
keys = ["a","d","q"]
client = MongoClient()

db = client.get_database("DATA")
# possible_collections = db.collection_names(include_system_collections=False)

db_met = client.get_database("Meta").get_collection("dataset_meta")
cursor = db_met.find({},{"db_col":1,"schema":1})
possible_collections = {}
for c in cursor:
    possible_collections[c["db_col"]] = c["schema"]

print "Possible collections: ", possible_collections.keys()

default_col_name = "Brexit_old"
col_name = raw_input("Which collection do you want to label ["+default_col_name+"]: ")
if col_name == "":
    col_name = default_col_name
while col_name not in possible_collections:
    print "Invalid collection name"
    col_name = raw_input("Which collection do you want to label: ")


schema_id = possible_collections[col_name]
print "Using collection '" + col_name + "' with schema '" + schema_id + "'"
db_col = db.get_collection(col_name)

default_left = "leave"
default_right = "remain"

left_arrow_label = raw_input("Label for (a) key [" +default_left+"]: ")
right_arrow_label = raw_input("Label for (d) key [" + default_right + "]: ")
if left_arrow_label == "":
    left_arrow_label = default_left
if right_arrow_label == "":
    right_arrow_label = default_right

while left_arrow_label == right_arrow_label:
    print "Labels should be different"
    left_arrow_label = raw_input("Label for (a) key [" +default_left+"]: ")
    right_arrow_label = raw_input("Label for (d) key [" + default_right + "]: ")

print "Using labels a->" + left_arrow_label + " and d->" + right_arrow_label
default_size = 1000
db_col_size = db_col.count()
size = raw_input("Number of tweets to sample [" + str(default_size) + "]: ")
if size == "":
    size = default_size
while size < 0:
    print "Size should be positve"
    size = int(raw_input("Number of tweets to sample: "))
while size > db_col_size:
    print "Warning size should be less than the collection count", db_col_size
    size = int(raw_input("Number of tweets to sample: "))
print "Going to sample " + str(size) + " tweets, re-running this program would produce duplicates"
# schema_id = raw_input("Schema: ")
# schemas = ["T4J","RAW"]
# while schema_id not in schemas:
#     print "Schema should be in ", schemas
#     schema_id = raw_input("Schema: ")
default_file_name = "labelling_out.dat"
file_name = raw_input("Label output file name [" + default_file_name + "]: ")
if file_name == "":
    file_name = default_file_name
print "Using output file: "+ file_name

print "Beginning sample"

sample_query = [
    {"$match": {Status.SCHEMA_MAP[schema_id]["language"]: "en"}},
    {"$sample":{"size":size}}
]

# t= progressbar.FormatCustomText("(" + left_arrow_label + " %(left)d, " +
#                                 right_arrow_label + " %(right)d, Unknown %(unk)d)", dict(left=0,right=0,unk=0))
# widgets = [t,":::", progressbar.Counter(),":::", progressbar.RotatingMarker()]
# bar = progressbar.ProgressBar(widgets=widgets)
cursor = db_col.aggregate(sample_query, allowDiskUse = True)
unknown_label = "unknown"
buffer = []
for i in cursor:
    buffer.append(i)
print "Buffer size", len(buffer)
with open(file_name,"a") as f:
    writer = csv.writer(f)
    print "Sampling finished beginning labelling"
    for i,c in enumerate(buffer):
        s = Status(c, schema_id)
        id = s.get_id()
        print  str(i) + " " + ("'" * 100)
        print id, s.get_text().replace("\n"," ")
        print s.get_hashtags()
        user_input = raw_input("Label (a:" + left_arrow_label + ",d:" + right_arrow_label + ","
                                                                                            "q:" + unknown_label+
                               "): ")
        while user_input not in keys:
            print "Invalid label key pressed, use 'exit' to quit"
            user_input = raw_input("Label (a:" + left_arrow_label + ",d:" + right_arrow_label + ","
                                                                                                "q:" + unknown_label+ "): ")
            if user_input == "exit":
                break
        if user_input == "a":
            writer.writerow([left_arrow_label,id])
        elif user_input == "d":
            writer.writerow([right_arrow_label, id])
        elif user_input == "q":
            writer.writerow([unknown_label, id])
        if divmod(i,10)[1] == 0:
            f.flush()
