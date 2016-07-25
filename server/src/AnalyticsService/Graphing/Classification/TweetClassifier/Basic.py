from AnalyticsService.Graphing.Classification.TweetClassifier.TweetScore import TweetScore


class BasicScoringSystem(object):
    def __init__(self, hashtags):
        self.hashtags = hashtags

    def predict(self, status):
        htags = status.get_hashtags()
        score = reduce(lambda x, y: x + y, map(lambda x: self.hashtags.get(x.lower(), 0.0), htags), 0.0)
        return TweetScore(-1 if score < 0 else 1, score)
