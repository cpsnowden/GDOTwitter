import logging
import abc

from AnalysisEngine.Analysis import Analysis


class EventAnalysis(Analysis):
    __metaclass__ = abc.ABCMeta
    _logger = logging.getLogger(__name__)
    __arguments = []

    def __init__(self, analytics_meta):
        super(EventAnalysis, self).__init__(analytics_meta)

    @abc.abstractmethod
    def process(self):
        pass

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(EventAnalysis, cls).get_args()

    @classmethod
    def get_classification(cls):
        return "Event Analysis"

    @classmethod
    def get_type(cls):
        pass
