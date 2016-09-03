import datetime

[{'$match': {'createdAt': {'$lte': datetime.datetime(2016, 6, 24, 2, 0, tzinfo=tzutc()), '$gte': datetime.datetime(
    2016, 6, 23, 2, 0, tzinfo=tzutc())}}}, {'$match': {'retweetedStatus.text': {'$ne': None, '$exists': True}}}, {
     '$group': {'count': {'$sum': 1}, '_id': '$retweetedStatus.user.screenName'}}, {'$sort': {'count': -1}}, {
     '$limit': 10}]
