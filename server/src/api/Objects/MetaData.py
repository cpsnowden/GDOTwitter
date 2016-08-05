import datetime
import yaml
from flask_restful import fields
from mongoengine import connect, Document, StringField, ListField, DateTimeField, LongField, DictField


with open("config.yml", 'r') as config_file:
    cfg = yaml.load(config_file)
mongo_settings = cfg["mongo"]

connect("Meta",
        alias="meta_data_db",
        host = mongo_settings["host"],
        port = mongo_settings["port"],
        username=mongo_settings["username"],
        password=mongo_settings["password"],
        authentication_source="admin")

class DatasetMeta(Document):
    description = StringField(required=True)
    tags = ListField(StringField())
    type = StringField(required=True)
    id = StringField(primary_key=True)
    db_col = StringField(required=True)
    status = StringField(required=True, default="ORDERED")
    start_time = DateTimeField(required=True, default=datetime.datetime.now())
    end_time = DateTimeField()
    collection_size = LongField(default=0)
    schema = StringField(default="RAW", choices=["RAW", "T4J"])

    meta = {"db_alias": "meta_data_db"}


class AnalyticsMeta(Document):
    description = StringField()
    classification = StringField(required=True)
    type = StringField(required=True)
    db_ref = StringField(required=True)
    status = StringField(required=True, default="ORDERED")
    dataset_id = StringField(required=True)
    id = StringField(primary_key=True)
    start_time = DateTimeField(required=True, default=datetime.datetime.now())
    end_time = DateTimeField()
    specialised_args = DictField()
    chart_id = StringField()
    graph_id = StringField()
    raw_id = StringField()
    meta = {"db_alias": "meta_data_db"}


class DictionaryWrap(fields.Raw):
    def format(self, value):
        return value
