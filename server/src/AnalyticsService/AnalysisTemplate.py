from Database.Persistence import DatabaseManager
from api.Objects.MetaData import DatasetMeta
import logging
from datetime import datetime
from AnalyticsService.Charting.Charting import CreateChart
class AnalysisTemplate(object):
    _logger = logging.getLogger(__name__)

    __arguments = [{"name": "startDateCutOff", "prettyName": "Start date cut-off", "type": "datetime",
                    "default_dataset_field": "start_time"},
                   {"name": "endDateCutOff", "prettyName": "End date cut-off", "type": "datetime",
                    "default_dataset_field": "end_time"}]

    @classmethod
    def get_args(cls):
        return cls.__arguments



    @classmethod
    def export_json(cls, analytics_meta, json, gridfs):

        analytics_meta.raw_id = "RAW_" + analytics_meta.db_ref
        analytics_meta.save()

        cls.write_json(json, analytics_meta.raw_id, gridfs)
        cls._logger.info("Saved analytics %s", analytics_meta.raw_id)
        analytics_meta.status = "SAVED"
        analytics_meta.end_time = datetime.now()
        analytics_meta.save()

    @classmethod
    def write_json(cls, data, name, gridfs):
        with gridfs.new_file(filename=name, content_type="text/json") as f:
            f.write(data)


    @classmethod
    def create_chart(cls, gridfs, analytics_meta, data):

        analytics_meta.status = "MAKING CHART"
        analytics_meta.save()

        analytics_meta.chart_id = "CHART_" + analytics_meta.db_ref

        html = CreateChart(data)

        with gridfs.new_file(filename=analytics_meta.chart_id, content_type="text/html") as f:
            f.write(html)

        analytics_meta.status = "CHART SAVED"
        analytics_meta.save()

    @classmethod
    def join_keys(cls, *keys):
        print keys
        return ".".join(keys)

    @classmethod
    def dollar_join_keys(cls, *keys):
        return "$" + cls.join_keys(*keys)
