class SVMUserModel(object):
    def __init__(self, classifier):
        self.classifier = classifier
        self.history = []
        self.h_length = 10

    def said(self, status):
        tweet_score = self.classifier.predict(status.get_text())
        self.history.append(tweet_score)
        return tweet_score.score

    def get_classification(self):
        return reduce(lambda x, y: x + y, map(lambda x: x.classification * abs(x.score), self.history[-self.h_length:]))
