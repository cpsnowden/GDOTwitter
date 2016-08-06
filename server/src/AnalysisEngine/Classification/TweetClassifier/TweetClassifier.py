import abc


class TweetClassifier(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def predict(self, status):
        return


class ClassificationScore(object):

    def __init__(self, classification, confidence):
        self.classification = classification
        self.confidence = confidence

    def __str__(self):
        return str(self.classification) + " " + str(self.confidence)
