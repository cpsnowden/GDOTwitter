import logging
import os

from AnalysisEngine.Classification.TweetClassifier.SVM import SVMClassifier
from AnalysisEngine.Classification.TweetClassifier.Basic import Basic
from AnalysisEngine.Classification.UserModel.UserModel import BasicUser, MovingAverageModel
DIR_NAME = os.path.dirname(__file__)


class ClassificationSystem(object):
    _logger = logging.getLogger(__name__)
    options = ["SVM", "BASIC"]
    users = {}

    def __init__(self, option, class_labels, data):

        self._logger.info("Using %s with labels %s and data %s", option, class_labels, data)

        self.classification_type = option
        self.tweet_classifier = None

        if option == "SVM":
            self.user_model = BasicUser
            self.tweet_classifier = SVMClassifier(class_labels,
                                                  os.path.join(DIR_NAME, "Training","TRAINING_DATA_OUT.csv"))
        elif option == "BASIC":
            self.user_model = BasicUser
            self.tweet_classifier = Basic(class_labels, data)

    def consume(self, status):

        user_id = status.get_user().get_id()
        if user_id not in self.users:
            self.users[user_id] = self.user_model(self.tweet_classifier)
        user = self.users[user_id]
        return user.said(status)
