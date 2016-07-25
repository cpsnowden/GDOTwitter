from AnalyticsService.TwitterObj import Status
from AnalyticsService.Graphing.Classification.User.ModelUser import SVMUserModel
from AnalyticsService.Graphing.Classification.User.Basic import BasicUserModel
from AnalyticsService.Graphing.Classification.TweetClassifier.Basic import BasicScoringSystem
from AnalyticsService.Graphing.Classification.TweetClassifier.SVM import SVMClassifier
import logging
import os


DIR_NAME = os.path.dirname(__file__)


class ClassificationSystem(object):
    _logger = logging.getLogger(__name__)
    options = ["SVM", "BASIC"]
    users = {}

    def __init__(self, option, hashtags):
        self.classification_type = option

        self.tweet_classifier = None

        if option == "SVM":
            self.user_model = SVMUserModel
            self._logger.info("Using SVM User Model")
            self.tweet_classifier = SVMClassifier({"leave": -1, "remain": 1}, False)
            self.tweet_classifier.train_from_csv(os.path.join(DIR_NAME,"TRAINING_DATA_OUT.csv"), -1)

        elif option == "BASIC":
            self._logger.info("Using Basic User Model")
            self.user_model = BasicUserModel
            self.tweet_classifier = BasicScoringSystem(hashtags)

    def consume(self, status):

        user_id = status.get_user().get_id()
        if user_id not in self.users:
            self.users[user_id] = self.user_model(self.tweet_classifier)

        user = self.users[user_id]
        tweet_score = user.said(status)
        return user.get_classification(), tweet_score
