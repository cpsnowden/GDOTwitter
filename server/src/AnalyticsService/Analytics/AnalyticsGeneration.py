import logging

from AnalyticsService.AnalysisGeneration import AnalysisGeneration

from AnalyticsService.Analytics.BasicStats.Original import Original
from AnalyticsService.Analytics.BasicStats.Languages import Languages
from AnalyticsService.Analytics.BasicStats.Hashtags import Hashtags
from AnalyticsService.Analytics.BasicStats.TimeZone import TimeZone

from AnalyticsService.Analytics.UserStats.TopAuthors import TopAuthors
from AnalyticsService.Analytics.UserStats.TopMentioned import TopMentioned
from AnalyticsService.Analytics.UserStats.TopRetweeted import TopRetweeted
from AnalyticsService.Analytics.UserStats.TopRetweeters import TopRetweeters

from AnalyticsService.Analytics.TimeStats.HashtagTimeDistribution import HashtagTimeDistribution
from AnalyticsService.Analytics.TimeStats.TweetTimeDist import TweetTimeDistribution
from AnalyticsService.Analytics.TimeStats.SentimentTimeDist import SentimentTimeDistribution
from AnalyticsService.Analytics.TimeStats.HashtagSentimentTimeDistribution import HashtagSentimentTimeDistribution
from AnalyticsService.Analytics.TimeStats.TimeZoneTimeDist import TimeZoneTimeDist


class AnalyticsGeneration(AnalysisGeneration):
    _logger = logging.getLogger(__name__)

    @classmethod
    def get_options(cls):
        return [Languages,
                Original,
                Hashtags,
                TimeZone,
                HashtagSentimentTimeDistribution,
                HashtagTimeDistribution,
                TweetTimeDistribution,
                SentimentTimeDistribution,
                TimeZoneTimeDist,
                TopAuthors,
                TopRetweeted,
                TopRetweeters,
                TopMentioned]

    @classmethod
    def get_classification(cls):
        return "Analytics"
