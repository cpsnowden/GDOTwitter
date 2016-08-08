from AnalysisEngine.Classification.TweetClassifier.TweetClassifier import TweetClassifier, ClassificationScore


class Basic(TweetClassifier):
    def __init__(self, class_labels, hashtags):
        self.hashtags = hashtags

    def predict(self, status):
        htags = status.get_hashtags()
        score = reduce(lambda x, y: x + y, map(lambda x: self.hashtags.get(x.lower(), 0.0), htags), 0.0)
        return ClassificationScore(1 if score > 0 else -1, abs(score))