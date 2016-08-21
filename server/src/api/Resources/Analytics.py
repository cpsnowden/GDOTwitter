import logging

from flask import make_response
from flask import request
from flask_restful import reqparse, marshal_with, fields, abort
from mongoengine.queryset import DoesNotExist

import api.Utils.MetaID as MetaID
from api.Auth import Resource
from api.Objects.MetaData import AnalyticsMeta, DatasetMeta, DictionaryWrap
from AnalysisEngine.AnalysisRouter import AnalysisRouter
from AnalysisEngine.AnalysisTasks import get_analytics

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
    "raw_id": fields.String,
    "uri_base": fields.Url("analytics"),
    "uri_data": fields.Url("analyticsData")
}

analytics_data_urls_fields = {
    "url_chart": fields.String(),
    "url_html": fields.String(),
    "url_raw": fields.String(),
    "url_graph": fields.String(),
}

analytics_data_fields = {
    "prefered_url" : fields.String(),
    "prefered_app": fields.String(),
    "urls": fields.Nested(analytics_data_urls_fields)
}


class AnalyticsDataOpt:
    def __init__(self, path, chart_id, html_id, raw_id, graph_id, prefered_url, prefered_app):
        self.prefered_url = prefered_url
        self.prefered_app = prefered_app
        self.urls = {}
        if chart_id is not None:
            self.urls["url_chart"] = path + "/dl?type=chart"
        else:
            self.urls["url_chart"] = None
        if html_id is not None:
            self.urls["url_html"] = path + "/dl?type=html"
        else:
            self.urls["url_html"] = None
        if raw_id is not None:
            self.urls["url_raw"] = path + "/dl?type=raw"
        else:
            self.urls["url_raw"] = None
        if graph_id is not None:
            self.urls["url_graph"] = path + "/dl?type=graph"
        else:
            self.urls["url_graph"] = None


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
            return

        if found.html_id is not None:
            r = self.dbm.deleteGridFSFile(found.html_id)
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
            return

        prefered_url, prefered_app = AnalysisRouter.get(found.classification, found.type).get_prefered_vis()
        return AnalyticsDataOpt(request.path, found.chart_id, found.html_id,
                                found.raw_id, found.graph_id, prefered_url,
                                prefered_app)


class AnalyticsDownload(Resource):
    logger = logging.getLogger(__name__)

    def __init__(self, **kwargs):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('type', type=str, help="Type of data", location='args',
                                 choices = ["graph","raw","chart","html"], required = True)
        self.dbm = kwargs["dbm"]

    def get(self, dataset_id, id):

        try:
            found = AnalyticsMeta.objects.get(id=id, dataset_id=dataset_id)
        except DoesNotExist:
            abort(404, message="Analytics {} does not exist".format(id))
            return

        args = self.parser.parse_args()
        dataType = args["type"]

        if dataType == "raw":
            self.logger.info("Get Raw DATA")
            f = self.dbm.gridfs.get_last_version(found.raw_id)
            response = make_response(f.read())
            response.headers["Content-Disposition"] = "attachment; filename = " + found.raw_id + ".json;"
            response.headers["mimetype"] = "application/json"
            return response
        elif dataType == "html":
            self.logger.info("Get HTML DATA")
            print found.html_id
            f = self.dbm.gridfs.get_last_version(found.html_id)
            response = make_response(f.read())
            response.headers["Content-Disposition"] = "attachment; filename = " + found.html_id + ".html;"
            response.headers["mimetype"] = "text/html"
            return response
        elif dataType == "chart":
            self.logger.info("Get Chart DATA")
            f = self.dbm.gridfs.get_last_version(found.chart_id)
            response = make_response(f.read())
            response.headers["Content-Disposition"] = "attachment; filename = " + found.chart_id + ".json;"
            response.headers["mimetype"] = "application/json"
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
        return AnalysisRouter.get_details()
