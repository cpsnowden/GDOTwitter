import logging
import abc

from AnalysisEngine.Analysis import Analysis


class Analytics(Analysis):
    __metaclass__ = abc.ABCMeta
    _logger = logging.getLogger(__name__)
    __arguments = []

    def __init__(self, analytics_meta):
        super(Analytics, self).__init__(analytics_meta)

    @abc.abstractmethod
    def process(self):
        pass

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(Analytics, cls).get_args()

    @classmethod
    def get_prefered_vis(cls):
        return "url_chart", "FusionChart"

    @classmethod
    def get_classification(cls):
        return "Analytics"

    @classmethod
    def get_type(cls):
        pass
