import abc


class UserModel(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, classifier):
        self.classifier = classifier

    @abc.abstractmethod
    def said(self, status):
        tweet_score = None
        user_score = None
        return user_score, tweet_score


class BasicUser(UserModel):
    POSITIVE = 40
    NEGATIVE = -40

    def __init__(self, classifier):
        super(BasicUser, self).__init__(classifier)

        self.time_constant = 5.0
        self.partisan = None
        self.score = 0.0
        self.scaler = 1.0

    def said(self, status):

        tweet_score = self.classifier.predict(status)
        tweet_score = tweet_score.classification * tweet_score.confidence

        if tweet_score > 0:
            self.add_positive(tweet_score)
        elif tweet_score < 0:
            self.add_negative(tweet_score)

        return self.score, tweet_score

    def add_positive(self, score):

        if self.partisan is None or self.partisan == "Negative":
            if self.partisan == "Negative":
                self.scaler = 2.0
            self.partisan = "Positive"

        self.score += self.scaler * score * (self.POSITIVE - self.score) / 100

    def add_negative(self, score):

        if self.partisan is None or self.partisan == "Positive":
            if self.partisan == "Positive":
                self.scaler = 2.0
            self.partisan = "Negative"

        self.score += self.scaler * abs(score) * (self.NEGATIVE - self.score) / 100


class MovingAverageModel(UserModel):

    def __init__(self, classifier):
        super(MovingAverageModel, self).__init__(classifier)

        self.history = []
        self.h_length = 10

    def said(self, status):

        tweet_score = self.classifier.predict(status.get_text())
        tweet_score = tweet_score.classification *  tweet_score.confidence
        self.history.append(tweet_score)
        return sum(self.history[-self.h_length:]), tweet_score
