import abc
import json
import logging
from datetime import datetime
from dateutil import parser
import yaml
import pymongo
from AnalysisEngine.Charting.Charting import create_chart
from AnalyticsService import Util
from AnalyticsService.TwitterObj import Status
from Database.Persistence import DatabaseManager
from api.Objects.MetaData import DatasetMeta

with open("config.yml", 'r') as config_file:
    cfg = yaml.load(config_file)["mongo"]


class Analysis(object):
    __metaclass__ = abc.ABCMeta
    _logger = logging.getLogger(__name__)
    __arguments = [{"name": "startDateCutOff",
                    "prettyName": "Start date cut-off",
                    "type": "datetime",
                    "default_dataset_field": "start_time"},
                   {"name": "endDateCutOff",
                    "prettyName": "End date cut-off",
                    "type": "datetime",
                    "default_dataset_field": "end_time"}]

    def __init__(self, analytics_meta):

        dataset_meta = DatasetMeta.objects.get(id=analytics_meta.dataset_id)
        self.analytics_meta  = analytics_meta
        self.dbm = DatabaseManager(cfg["username"], cfg["password"], cfg["host"], cfg["port"])
        self.col = self.dbm.data_db.get_collection(dataset_meta.db_col)
        self.args = self.parse_args(analytics_meta.specialised_args, dataset_meta)
        self.schema = dataset_meta.schema
        self._logger.info("Attempting to run %s with arguments %s", self.get_type, self.args)

    @abc.abstractmethod
    def process(self):
        return

    @classmethod
    def get_args(cls):
        return cls.__arguments

    @classmethod
    def get_classification(cls):
        pass

    @classmethod
    def get_type(cls):
        return

    def parse_args(self, posted_args, dataset_meta):

        args = {}
        for arg in self.get_args():
            if "default" in arg:
                args[arg["name"]] = arg["default"]
            if "default_dataset_field" in arg:
                args[arg["name"]] = dataset_meta[arg["default_dataset_field"]]

        for arg_name, value in posted_args.iteritems():
            if arg_name in args:
                args[arg_name] = value
        return args

    def get_time_bounded_query(self, query):

        if type(self.args["startDateCutOff"]) is datetime:
            self._logger.info("Using datetime fields")
            start = self.args["startDateCutOff"]
            end = self.args["endDateCutOff"]
        else:
            self._logger.info("Using string datetime conversion")
            start = parser.parser(self.args["startDateCutOff"])
            end = parser.parser(self.args["endDateCutOff"])

        query[Status.SCHEMA_MAP[self.schema]["ISO_date"]] = {"$gte": start,
                                                             "$lte": end}

        return query

    def get_sorted_cursor(self, query, limit, projection=None):

        if projection is None:
            projection = {}
        self._logger.info("Querying DATA database, collection %s with query %s", self.col.name, query)

        # if limit > 0:
        cursor = self.col.find(query, projection).limit(limit) \
            .sort(Status.SCHEMA_MAP[self.schema]["ISO_date"], pymongo.ASCENDING)
        # else:
        #     cursor = self.col.find(query) \
        #         .sort(Status.SCHEMA_MAP[self.schema]["ISO_date"], pymongo.ASCENDING)

        cusor_size = cursor.count(with_limit_and_skip=True)

        self._logger.info("Cursor size %d", cusor_size)
        if cusor_size == 0:
            self._logger.warning("Cursor has no data")
            return None

        return cursor

    def export_json(self, data):

        self.analytics_meta.status = "EXPORTING JSON"
        self.analytics_meta.save()

        self.analytics_meta.raw_id = "RAW_" + self.analytics_meta.db_ref

        with self.dbm.gridfs.new_file(filename=self.analytics_meta.raw_id, content_type="text/json") as f:
            f.write(json.dumps(data, default = Util.date_encoder))

        self.analytics_meta.status = "SAVED"
        self.analytics_meta.end_time = datetime.now()
        self.analytics_meta.save()

    def export_chart(self, data):

        self.analytics_meta.status = "EXPORTING CHART"
        self.analytics_meta.save()

        self.analytics_meta.chart_id = "CHART_" + self.analytics_meta.db_ref

        html = create_chart(data)

        with self.dbm.gridfs.new_file(filename=self.analytics_meta.chart_id, content_type="text/html") as f:
            f.write(html)

        self.analytics_meta.status = "CHART SAVED"
        self.analytics_meta.save()
