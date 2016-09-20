import datetime
import yaml
from flask_restful import fields
from mongoengine import connect, Document, StringField, ListField, DateTimeField, LongField, DictField, BooleanField


with open("config.yml", 'r') as config_file:
    cfg = yaml.load(config_file)
request_db = cfg["mongo"]["requests"]

connect(request_db["name"],
        alias="meta_data_db",
        host = request_db["host"],
        port = request_db["port"],
        username=request_db["username"],
        password=request_db["password"],
        authentication_source=request_db["auth_db"])

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
    html_id = StringField()
    chart_id = StringField()
    graph_id = StringField()
    raw_id = StringField()
    prefered_url = StringField()
    prefered_app = StringField()
    gdo_enabled = BooleanField()
    meta = {"db_alias": "meta_data_db"}


class Slides(Document):
    id = StringField(primary_key=True)
    description = StringField()
    sections = ListField()
    meta = {"db_alias": "meta_data_db"}

class DictionaryWrap(fields.Raw):
    def format(self, value):
        return value
