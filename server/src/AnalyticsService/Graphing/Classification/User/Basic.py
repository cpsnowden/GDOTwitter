class BasicUserModel(object):
    POSITIVE = 40
    NEGATIVE = -40

    def __init__(self, tweet_classifier):

        self.tweet_classifier = tweet_classifier
        self.time_constant = 5.0
        self.partisan = None
        self.score = 0.0
        self.scaler = 1.0

    def said(self, status):

        score = self.tweet_classifier.predict(status).score

        if score > 0:
            self.add_positive(score)
        elif score < 0:
            self.add_negative(score)

        return score


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

    def get_classification(self):
        return self.score