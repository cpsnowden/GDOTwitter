import numpy as np


class TweetScoring(object):

    @staticmethod
    def get_exp_score(a_score, b_score, MAX_TWEET_SCORE, time_constant = 2.0, ):
        return MAX_TWEET_SCORE * (- np.exp(-a_score / time_constant) + np.exp(-b_score / time_constant))

    @staticmethod
    def get_binary_score(a_score, b_score, MAX_TWEET_SCORE):

        if a_score > b_score:
            return MAX_TWEET_SCORE
        elif b_score > a_score:
            return -MAX_TWEET_SCORE
        else:
            return 0.0


class TwitterUserModel(object):

    MAX_USER_SCORE = 100

    scoring_options = {
        "Exponential": TweetScoring.get_exp_score,
        "HardBinary": TweetScoring.get_binary_score
    }

    def __init__(self, hashtag_scores, n = 10, scoring_system = "Exponential"):

        self.A, self.B = hashtag_scores

        self.scoring_function = self.scoring_options.get(scoring_system)

        self.score = 0.0
        self.history = []
        self.n = n
        self.MAX_TWEET_SCORE = self.MAX_USER_SCORE / float(self.n)

    def said_these(self, hashtags):
        tweet_score = self.get_tweet_score(hashtags)
        self.score = self.get_user_score(tweet_score)
        return self.score

    def get_user_score(self, new_score):
        self.history.append(new_score)
        self.history = self.history[-self.n:]
        return sum(self.history)

    def get_tweet_score(self, hashtags):
        A_score = reduce(lambda x, y: x + y, map(lambda h: float(self.A.get(h.lower(), 0.0)), hashtags), 0.0)
        B_score = reduce(lambda x, y: x + y, map(lambda h: float(self.B.get(h.lower(), 0.0)), hashtags), 0.0)

        return self.scoring_function(A_score, B_score, self.MAX_TWEET_SCORE)