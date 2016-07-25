import logging

from AnalyticsService.AnalysisGeneration import AnalysisGeneration
from AnalyticsService.Graphing.Community.CommunityGraphClassification import CommunityGraphClassification
from AnalyticsService.Graphing.Time.HashtagGraph import HashtagGraph
from AnalyticsService.Graphing.Time.HashtagGraphRetweet import HashtagGraphRetweet
from AnalyticsService.Graphing.Time.HashtagGraphRetweetTwoNode import HashtagGraphRetweetTwoNode

from AnalyticsService.Graphing.Time.TimeHashtagRetweet import TimeHashtagRetweet

class GraphGeneration(AnalysisGeneration):
    _logger = logging.getLogger(__name__)

    @classmethod
    def get_options(cls):
        return [HashtagGraph,
                HashtagGraphRetweet,
                HashtagGraphRetweetTwoNode,
                CommunityGraphClassification,
                TimeHashtagRetweet]

    @classmethod
    def get_classification(cls):
        return "Graph"