from logging.handlers import RotatingFileHandler

import flask_restful
import yaml
from DataService.DataService import DataService
from Database.Persistence import DatabaseManager
from api.Resources.Root import RootResource
from api.Resources.Analytics import *
from api.Resources.DataSet import DataSet, DatasetList, DatasetStatus, DataServiceR
from api.Resources.TwitterConsumer import TwitterConsumer, TwitterConsumerList
from api.Resources.GDOSlide import SlideList, Slide
from flask import Flask


my_handler = RotatingFileHandler('server.log', mode='a', maxBytes=5 * 1024 * 1024,
                                 backupCount=2, encoding=None, delay=0)
my_handler.setLevel(logging.INFO)
root_logger = logging.getLogger("")
root_logger.addHandler(my_handler)
root_logger.setLevel(logging.INFO)

app = Flask(__name__)
api = flask_restful.Api(app, prefix="/API")

with open("config.yml", 'r') as config_file:
    cfg = yaml.load(config_file)
mongo_settings = cfg["mongo"]

dbm = DatabaseManager(mongo_settings["raw"], mongo_settings["results"])
data_service = DataService(dbm, cfg["data_service_cfg"])

api.add_resource(RootResource,
                 "",
                 endpoint = "root")

api.add_resource(DatasetList, '/dataset',
                 resource_class_kwargs={'data_service': data_service},
                 endpoint = "dataSetList")

api.add_resource(DataSet,
                 '/dataset/<string:id>',
                 resource_class_kwargs={'data_service': data_service},
                 endpoint = "dataSet")

api.add_resource(DatasetStatus,
                 '/dataset/<string:id>/status',
                 resource_class_kwargs={'data_service': data_service},
                 endpoint = "dataSetStatus")

api.add_resource(AnalyticsList,
                 '/dataset/<string:id>/analytics',
                 endpoint = "analyticsList")

api.add_resource(Analytics,
                 '/dataset/<string:dataset_id>/analytics/<string:id>',
                 resource_class_kwargs={'dbm': dbm},
                 endpoint = "analytics")

api.add_resource(AnalyticsData,
                 '/dataset/<string:dataset_id>/analytics/<string:id>/data',
                 endpoint="analyticsData")

api.add_resource(AnalyticsDownload,
                 '/dataset/<string:dataset_id>/analytics/<string:id>/data/dl',
                 resource_class_kwargs={'dbm': dbm},
                 endpoint="analyticsDataDownload")

api.add_resource(TwitterConsumer,
                 '/twitter_consumer/<int:id>',
                 resource_class_kwargs={'twitter_service': data_service.twitter_service},
                 endpoint="twitterConsumer")

api.add_resource(TwitterConsumerList,
                 '/twitter_consumer',
                 resource_class_kwargs={'twitter_service': data_service.twitter_service},
                 endpoint = "twitterConsumerList")

api.add_resource(DataServiceR,
                 '/data_service',
                 resource_class_kwargs={'data_service': data_service},
                 endpoint = "dataServiceList")

api.add_resource(AnalyticsOptions, '/analytics_options',
                 endpoint = "analyticsOptions")

api.add_resource(SlideList, '/slide',
                 endpoint="slideList")

api.add_resource(Slide, '/slide/<string:id>',
                 endpoint="slide")

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host = "0.0.0.0", threaded=True)
