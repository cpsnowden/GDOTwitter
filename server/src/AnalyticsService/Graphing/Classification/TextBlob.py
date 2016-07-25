from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer


blob = TextBlob("#VoteRemain let's not be stupid now.", analyzer=NaiveBayesAnalyzer())

print blob.sentiment