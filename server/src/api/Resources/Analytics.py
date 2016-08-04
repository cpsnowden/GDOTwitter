import logging

import gridfs
import api.Utils.MetaID as MetaID
from flask import make_response
from flask_restful import reqparse, marshal_with, fields, abort
from mongoengine.queryset import DoesNotExist
from flask import request
from AnalyticsService.AnalyticsTasks import get_analytics
from AnalyticsService.AnalyticsEngine import AnalyticsEngine
from api.Auth import Resource
from api.Objects.MetaData import AnalyticsMeta, DatasetMeta, DictionaryWrap

analytics_meta_fields = {
    "type": fields.String,
    "id": fields.String(attribute="id"),
    "dataset_id": fields.String(),
    "start_time": fields.DateTime(attribute="start_time"),
    "end_time": fields.DateTime(attribute="end_time"),
    "status": fields.String,
    "db_ref": fields.String,
    "specialised_args": DictionaryWrap(attribute="specialised_args"),
    "classification": fields.String,
    "description": fields.String,
    "uri_base": fields.Url("analytics"),
    "uri_data": fields.Url("analyticsData")
}

analytics_data_fields = {
    "url_chart": fields.String(),
    "url_raw": fields.String(),
    "url_graph": fields.String(),
}


class AnalyticsDataOpt:
    def __init__(self, path, chart_id, raw_id, graph_id):
        if chart_id is not None:
            self.url_chart = path + "/dl?type=chart"
        else:
            self.url_chart = None
        if raw_id is not None:
            self.url_raw = path + "/dl?type=raw"
        else:
            self.url_raw = None
        if graph_id is not None:
            self.url_graph = path + "/dl?type=graph"
        else:
            self.url_graph = None


class AnalyticsList(Resource):
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('type', type=str, help="Type of analytics")
        self.parser.add_argument('specialised_args', type=dict, help="Specialised Arguments")
        self.parser.add_argument('classification', type=str, help="Classification of analytics")
        self.parser.add_argument('description', type=str, help="Description of analytics")

    @marshal_with(analytics_meta_fields)
    def get(self, id):
        return [i._data for i in AnalyticsMeta.objects(dataset_id=id)]

    @marshal_with(analytics_meta_fields)
    def post(self, id):
        args = self.parser.parse_args()

        dataset_meta = DatasetMeta.objects.get(id=id)

        short_id, long_id = MetaID.get_id(dataset_meta.db_col, prefix="A_")

        analytics_meta = AnalyticsMeta(classification=args["classification"],
                                       type=args["type"],
                                       description=args["description"],
                                       dataset_id=id,
                                       db_ref = short_id,
                                       id=long_id,
                                       specialised_args=args["specialised_args"])

        analytics_meta.save()

        get_analytics.delay(analytics_meta.id)

        return analytics_meta._data


class Analytics(Resource):
    logger = logging.getLogger(__name__)

    def __init__(self, **kwargs):

        self.dbm = kwargs["dbm"]

    @marshal_with(analytics_meta_fields)
    def get(self, dataset_id, id):

        try:
            return AnalyticsMeta.objects.get(id=id, dataset_id=dataset_id)._data
        except DoesNotExist:
            abort(404, message="Analytics {} does not exist".format(id))

    def delete(self, dataset_id, id):

        try:
            found = AnalyticsMeta.objects.get(id=id, dataset_id=dataset_id)
        except DoesNotExist:
            abort(404, message="Analytics {} does not exist".format(id))

        if found.chart_id is not None:
            r = self.dbm.deleteGridFSFile(found.chart_id)
        if found.graph_id is not None:
            r = self.dbm.deleteGridFSFile(found.graph_id)
        if found.raw_id is not None:
            r = self.dbm.deleteGridFSFile(found.raw_id)

        found.delete()

        return "", 204


class AnalyticsData(Resource):
    logger = logging.getLogger(__name__)

    @marshal_with(analytics_data_fields)
    def get(self, dataset_id, id):

        try:
            found = AnalyticsMeta.objects.get(id=id, dataset_id=dataset_id)
        except DoesNotExist:
            abort(404, message="Analytics {} does not exist".format(id))

        return AnalyticsDataOpt(request.path, found.chart_id, found.raw_id, found.graph_id)


class AnalyticsDownload(Resource):
    logger = logging.getLogger(__name__)

    def __init__(self, **kwargs):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('type', type=str, help="Type of data", location='args',
                                 choices = ["graph","raw","chart"], required = True)
        self.dbm = kwargs["dbm"]

    def get(self, dataset_id, id):

        try:
            found = AnalyticsMeta.objects.get(id=id, dataset_id=dataset_id)
        except DoesNotExist:
            abort(404, message="Analytics {} does not exist".format(id))

        args = self.parser.parse_args()
        dataType = args["type"]

        if dataType == "raw":
            self.logger.info("Get Raw DATA")
            f = self.dbm.gridfs.get_last_version(found.raw_id)
            response = make_response(f.read())
            response.headers["Content-Disposition"] = "attachment; filename = " + found.raw_id + ".json;"
            response.headers["mimetype"] = "application/json"
            return response
        elif dataType == "chart":
            self.logger.info("Get Chart DATA")
            f = self.dbm.gridfs.get_last_version(found.chart_id)
            response = make_response(f.read())
            response.headers["Content-Disposition"] = "attachment; filename = " + found.chart_id + ".html;"
            response.headers["mimetype"] = "text/html"
            return response
        elif dataType == "graph":
            self.logger.info("Get Graph DATA")
            f = self.dbm.gridfs.get_last_version(found.graph_id)
            response = make_response(f.read())
            response.headers["Content-Disposition"] = "attachment; filename = " + found.graph_id + ".graphml;"
            response.headers["mimetype"] = "text/plain"
            return response
        else:
            self.logger.error("Why am I here")
            abort(404, message="Should never get here")


class AnalyticsOptions(Resource):
    logging = logging.getLogger(__name__)

    def get(self):
        return AnalyticsEngine.get_details()
