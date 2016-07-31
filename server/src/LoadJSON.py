from pymongo import MongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError
import progressbar
from dateutil import parser
import json
import os

db = MongoClient().get_database("DATA")
twitter = db.get_collection("Twitter_Breixt_9month")
facebook = db.get_collection("Facebook_Breixt_9month")

twitter.create_index([("ISO_created_at", ASCENDING)])
twitter.create_index([("_id", ASCENDING)], unique=True)
facebook.create_index([("ISO_created_at", ASCENDING)])
facebook.create_index([("_id", ASCENDING)], unique=True)

def reader(stream):
    for line in stream:
        yield json.loads(line)

TwitterSCHEMA = {"id":"_id", "date":"postedTime", "db":twitter}
FacebookSHEMA = {"id":"_id", "date":"pub_date", "db": facebook}
schemas = {"twitter":TwitterSCHEMA,"facebook":FacebookSHEMA}

# path = "/Users/ChrisSnowden/Downloads/2016.01.json"

base_path = "/home/ubuntu/ext/DATA/BREXIT_SUPER_LARGE"
files = [
    "2016.01.json",
    "2016.02.json",
    "2016.03.json",
    "2016.04.json",
    "2016.05.json",
    "2016.06.01.json",
    "2016.06.02.json",
    "2016.06.03.json",
    "2016.06.04.json",
    "2016.06.05.json",
    "2016.06.06.json",
    "2016.06.07.json",
    "2016.06.08.json",
    "2016.06.09.json",
    "2016.06.10.json",
    "2016.06.11.json",
    "2016.06.12.json",
    "2016.06.13.json",
    "2016.06.14.json",
    "2016.06.15.json",
    "2016.06.16.json",
    "2016.06.17.json",
    "2016.06.18.json",
    "2016.06.19.json",
    "2016.06.20.json",
    "2016.06.21.json",
    # "2016.06.22.json",
    # "2016.06.23.json",
    # "2016.06.24.json",
    # "2016.06.25.json",
    # "2016.06.26.json",
    # "2016.06.27.json",
    # "2016.06.28.json",
    # "2016.06.29.json",
    # "2016.06.30.json"
    ]
abs_files = [os.path.join(base_path, f) for f in files]

def load(file):
    print "Loading file", file
    bar = progressbar.ProgressBar()
    for i in bar(reader(open(file))):
        source = i["source"]
        if source not in schemas:
            print "WARNING UNKNOWN SOURCE, SKIPPING: ", source
            continue

        schema = schemas[source]

        date_string = i[schema["date"]]
        date = parser.parse(date_string)
        i["ISO_created_at"] = date

        try:
            result = schema["db"].insert_one(i)
        except DuplicateKeyError:
            print i,"Ignore duplicate"
            continue
        # print  source, date, result.inserted_id
    bar.finish()

    print "Removing file to save space"
    try:
        os.remove(file)
    except OSError:
        print "Couldn't remove", file

for f in abs_files:
    load(f)