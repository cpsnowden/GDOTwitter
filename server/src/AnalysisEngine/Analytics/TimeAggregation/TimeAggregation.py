import logging
import abc
from AnalysisEngine.Analytics.Analytics import Analytics
import datetime


class TimeAggregation(Analytics):
    __metaclass__ = abc.ABCMeta

    _logger = logging.getLogger(__name__)
    _options = ["Minute", "Hour", "Day", "Week"]
    __arguments = [{"name": "timeInterval",
                    "prettyName": "Time interval",
                    "type": "enum",
                    "options": _options,
                    "default": "Hour"}]

    def __init__(self, analytics_meta):
        super(TimeAggregation, self).__init__(analytics_meta)

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(TimeAggregation, cls).get_args()

    def get_time_values(self, start, end):
        t_values = []
        date = start
        while date <= end:
            t_values.append(date)
            date += datetime.timedelta(**{self.args["timeInterval"].lower() + "s": 1})

        return t_values
