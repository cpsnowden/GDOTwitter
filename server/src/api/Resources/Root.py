import logging
from flask_restful import marshal_with, fields
from flask import request
from api.Auth import Resource

root_fields = {
    "uri_data_set": fields.Url("dataSetList", scheme="http"),
    "uri_twitter_consumer": fields.Url("twitterConsumerList", scheme="http"),
    "uri_data_service": fields.Url("dataServiceList", scheme="http"),
    "uri_analysis_options": fields.Url("analyticsOptions", scheme="http"),
    "uri_slides": fields.Url("slideList", scheme="http"),
    "msg": fields.String,
    "healthy": fields.Boolean
}


class RootResource(Resource):
    logger = logging.getLogger(__name__)

    @marshal_with(root_fields)
    def get(self):

        # address = request.remote_addr
        return {"msg": "Connected to the GDO Twitter API", "healthy":True}
