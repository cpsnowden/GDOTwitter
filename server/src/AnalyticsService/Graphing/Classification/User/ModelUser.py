class SVMUserModel(object):
    def __init__(self, classifier):
        self.classifier = classifier
        self.history = []
        self.h_length = 10

    def said(self, status):
        tweet_score,_ = self.classifier.get(status.get_text())
        self.history.append(tweet_score)
        return tweet_score.score

    def get_classification(self):
        return reduce(lambda x, y: x + y, map(lambda x: x.classification * abs(x.score), self.history[-self.h_length:]))

#
# classifier = SVMClassifier({"leave": 0, "remain": 1}, False)
#
# # print classifier.tokenizer.tokenize("50,000 :),")
#
# classifier.train_from_csv("../TRAINING_DATA.csv", -1)
#
# adam = SVMUserModel(classifier)
# adam.said()
