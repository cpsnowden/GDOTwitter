import operator


class CommunityUser(object):

    UNCLASSIFIED = "Unclassified"

    def __init__(self, classification_scores):
        self.classifications = dict([(c,0.0) for c in classification_scores.keys()])
        self.classification_scores = classification_scores
        self.status_ids = []
        self.number_of_times_retweets = 0.0
        self.number_of_times_mentioned = 0.0

    @property
    def get_classification(self):

        max_score = max(self.classifications.iteritems(), key = operator.itemgetter(1))[1]
        maxes = [c for (c,s) in self.classifications.items() if s == max_score]
        if len(maxes) > 1:
            return self.UNCLASSIFIED
        return maxes[0]

    def said(self, status):

        sid = str(status.get_id())
        if sid in self.status_ids:
            return self.get_classification

        self.status_ids.append(sid)

        hashtags = status.get_hashtags()

        for classification in self.classifications.keys():
            self.classifications[classification] += \
                self.get_score(hashtags, self.classification_scores[classification])
        return self.get_classification

    def retweeted_by(self, user):

        u_cls = user.get_classification
        if u_cls is not self.UNCLASSIFIED:
            self.classifications[u_cls] += 3
        self.number_of_times_retweets += 1
        return self.get_classification

    def get_number_statuses(self):
        return len(self.status_ids)

    def mentioned(self):
        self.number_of_times_mentioned +=1

    @staticmethod
    def get_score(hashtags, scores):
         return reduce(lambda x,y:x+y,map(lambda h: 1.0 if h.lower() in scores else 0.0, hashtags), 0.0)