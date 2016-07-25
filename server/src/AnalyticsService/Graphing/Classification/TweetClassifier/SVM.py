import csv
import operator
import re
from collections import OrderedDict
import logging
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.tokenize import TweetTokenizer
from sklearn import metrics
from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from textblob.base import BaseTokenizer
from AnalyticsService.Graphing.Classification.TweetClassifier.TweetScore import TweetScore

emoticon_string = r"""(?:
[<>]?
[:;=8]                     # eyes
[\-o\*\']?                 # optional nose
[\)\]\(\[dDpP/\:\}\{@\|\\] # mouth
|
[\)\]\(\[dDpP/\:\}\{@\|\\] # mouth
[\-o\*\']?                 # optional nose
[:;=8]                     # eyes
[<>]?
)"""

class TweetPreprocessor(BaseTokenizer):

    twt_tknzr = TweetTokenizer(preserve_case=False, reduce_len=True, strip_handles=True)
    url_reg = re.compile(r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))')
    txt_reg = re.compile(r'.*[A-Za-z].*|' + emoticon_string,re.VERBOSE | re.I | re.UNICODE)
    hashtags = re.compile(r"""(?:\#+[\w_]+[\w\'_\-]*[\w_]+)""")
    lemmatizer = nltk.WordNetLemmatizer()

    def tokenize(self, text):
        # print text
        tokens = self.twt_tknzr.tokenize(text)
        tokens = [i.lower() for i in tokens if i not in stopwords.words("english")]
        tokens = [i for i in tokens if self.txt_reg.match(i) and i not in ["rt"]]
        tokens = [i for i in tokens if not self.url_reg.match(i)]
        # tokens = [i.lstrip("#") for i in tokens if self.hashtags.match(i)]
        # for t in tokens:
        #     token_temp = []
        #     if self.hashtags.match(t):
        #         replacement = t.lstrip("#")
        #         token_temp.append(replacement)
        #     else:
        #         token_temp.append(t)

        tokens = [self.lemmatizer.lemmatize(i,
                                            {'N': wn.NOUN,
                                             'V': wn.VERB,
                                             'R': wn.ADV,
                                             'J': wn.ADJ
                                            }.get(t[0], wn.NOUN))
                  for (i, t) in nltk.pos_tag(tokens)]
        # print tokens
        # print
        return tokens

class SVMClassifier(object):
    _logger = logging.getLogger(__name__)

    def __init__(self, class_mapping, tfid = False):
        self.class_mapping = class_mapping
        self.reverse_mapping = {v: k for k, v in self.class_mapping.items()}
        self.clf = svm.SVC(kernel='linear')
        self.preprocessor = TweetPreprocessor()
        self.feature_list = None
        self.tokenizer = TweetPreprocessor()
        self.tfid = tfid
        if tfid:
            self.cv = TfidfVectorizer(tokenizer=self.tokenizer.tokenize, max_features=500)
        else:
            self.cv = CountVectorizer(tokenizer=self.tokenizer.tokenize, max_features=500)

    def get(self, status):
        feature_vector = self.cv.transform([status])

        classification = self.clf.predict(feature_vector)
        score = self.clf.decision_function(feature_vector)

        return TweetScore(classification[0], score[0]), feature_vector

    def train(self, data, labels):
        self._logger.info("Attempting to train the SVM classifier")
        label_numbers = [self.class_mapping[i] for i in labels]
        training_data = self.cv.fit_transform(data)
        self.clf.fit(training_data, label_numbers)
        self._logger.info("Using features: " + str(self.get_features()))

    def get_features(self):
        if self.tfid and hasattr(self.cv, "idf_"):
            d = dict(zip(self.cv.get_feature_names(), self.cv.idf_))
            return OrderedDict(sorted(d.items(), key=operator.itemgetter(1)))
        else:
            return self.cv.get_feature_names()

    def train_from_csv(self, path, row_count = -1):
        self._logger.info("Attempting to get training data from training file: " + path)
        data = csv.reader(open(path, 'rb'), delimiter=',', quotechar='|')
        labels = []
        text = []
        try:
            for i,row in enumerate(data):

                if 0 < row_count < i:
                    break
                labels.append(row[0])
                text.append(row[1])
        except IndexError:
            print i
            exit()

        self.train(text, labels)

    def test_from_csv(self, path, row_count = -1):

        data = csv.reader(open(path, 'rb'), delimiter=',', quotechar='|')
        true_labels = []
        predicted_labels = []
        for i, row in enumerate(data):
            if 0 < row_count < i:
                break
            truth = self.class_mapping[row[0]]
            score, fv = self.get(row[1])
            predicted = score.classification
            predicted_labels.append(predicted)
            true_labels.append(truth)
            if truth != predicted:
                print "================================================================"
                print "Truth:",self.reverse_mapping[truth],"Predicted:",self.reverse_mapping[predicted],row[1]
                print fv
                print "================================================================"

        return metrics.classification_report(true_labels, predicted_labels, target_names=self.class_mapping.keys())


    def get_informative_features(self, n = 30):

        tvec = self.clf.coef_
        coefs = sorted(
            zip(tvec[0].toarray()[0], self.cv.get_feature_names()),
            key=operator.itemgetter(0), reverse=True
        )
        topn = zip(coefs[:n], coefs[:-(n + 1):-1])
        output = []
        print topn
        # Create two columns with most negative and most positive features.
        for (cp, fnp), (cn, fnn) in topn:
            output.append(
                "{:0.4f}{: >15}    {:0.4f}{: >15}".format(
                    cp, fnp, cn, fnn
                )
            )

        return "\n".join(output)


if __name__ == '__main__':

    # c = TweetPreprocessor()
    # print c.tokenize("Tweeting from the UK city that's closest to the EU continent. Hoping for a #Bremain result "
    #              "tomorrow! #EUref https://t.co/vfRYSagnma")
    # exit()
    # path = "../TEST_DATA.csv"
    # writer = csv.writer(open("../TEST_DATA_OUT.csv","w"), delimiter=',', quotechar='|', quoting=csv.QUOTE_ALL)
    # data = csv.reader(open(path, 'rb'), delimiter=',', quotechar='|')
    #
    # for row in data:
    #     if "RT" in row[1]:
    #         continue
    #     else:
    #         writer.writerow(row)
    # exit()
    import pprint
    classifier = SVMClassifier({"leave":0,"remain":1}, False)

    # print classifier.tokenizer.tokenize("50,000 :),")

    classifier.train_from_csv("../TRAINING_DATA_OUT.csv", -1)




    pprint.pprint(classifier.get_features())
    print classifier.get_informative_features()

    # print classifier.test_from_csv("../TEST_DATA.csv", -1)


