import logging

from AnalyticsService.AnalysisGeneration import AnalysisGeneration
from AnalyticsService.Graphing.Community.CommunityGraphClassification import CommunityGraphClassification
from AnalyticsService.Graphing.Time.HashtagTimeGraph import HashtagTimeGraph
from AnalyticsService.Graphing.Time.HashtagGraphRetweet import HashtagGraphRetweet
from AnalyticsService.Graphing.Time.HashtagGraphRetweetTwoNode import HashtagGraphRetweetTwoNode
from AnalyticsService.Graphing.Time.TimeHashtagRetweet import TimeHashtagRetweet

from AnalyticsService.Graphing.Hashtag.HashtagCollocationGraph import HashtagCollocationGraph


class GraphGeneration(AnalysisGeneration):
    _logger = logging.getLogger(__name__)

    @classmethod
    def get_options(cls):
        return [HashtagTimeGraph,
                HashtagGraphRetweet,
                HashtagGraphRetweetTwoNode,
                HashtagCollocationGraph,
                CommunityGraphClassification,
                TimeHashtagRetweet]

    @classmethod
    def get_classification(cls):
        return "Graph"
