class TweetScore(object):
    def __init__(self, classification, score):
        self.classification = classification
        self.score = score

    def __str__(self):
        return str(self.classification) + " " + str(self.score)