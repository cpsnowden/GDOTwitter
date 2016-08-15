import json
import logging
from collections import OrderedDict

from dateutil import parser

from AnalysisEngine.Analytics.Analytics import Analytics
from AnalysisEngine.Analytics.EventDetection.EventDetection import EventDetection

class HashtagEventDetection(Analytics):
    _logger = logging.getLogger(__name__)
    __arguments = [dict(name="hashtag_rate_f_name", prettyName="Name of gridfs file with hashtag rates", type="string",
                        default="blah"),
                   dict(name="hashtag", prettyName="Hashtag", type="enum", options=["strongerin",
                                                                                                 "brexit",
                                                                                                 "voteleave"],
                        default="strongerin")]

    def __init__(self, analytics_meta):
        super(HashtagEventDetection, self).__init__(analytics_meta)

    @classmethod
    def get_type(cls):
        return "Hashtag Event Detection"

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(HashtagEventDetection, cls).get_args()

    def process(self):

        f_name = self.args["hashtag_rate_f_name"]
        hashtag = self.args["hashtag"]

        f = self.dbm.gridfs.get_last_version(f_name)

        raw_data = json.load(f)
        hashtags = [i["_id"] for i in raw_data["data"]["values"]]

        if hashtag not in hashtags:
            return False

        x_categories = [parser.parse(i) for i in raw_data["data"]["categories"]]
        y_labels = OrderedDict.fromkeys(x_categories, 0)

        series = filter(lambda x: x["_id"] == hashtag, raw_data["data"]["values"])[0]

        for entry in series["data"]:
            y_labels[parser.parse(entry["dt"])] = entry["count"]

        eventDetector = EventDetection(self.col, "4d547cbd-99e2-4b00-a40e-987c67c252b8")
        events = eventDetector.map_events(series, hashtag, self.schema)

        result = {"details": {"chartType": "event",
                              "chartProperties": {"yAxisName": "Tweets per hour",
                                                  "xAxisName": "Date (UTC)",
                                                  "caption": self.dataset_meta.description,
                                                  "subcaption": ""}},
                  "data": {"series": series, "events": events}}

        self.export_chart(result)
        self.export_json(result)

        return True
