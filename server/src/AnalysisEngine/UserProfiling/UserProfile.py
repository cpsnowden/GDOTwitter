import datetime

class UserProfile(object):

    def __init__(self, screenName, dataSetName):
        self.profileImage = None
        self.name = ""
        self.screenName = "@" + screenName
        self.description = ""
        self.createdAt = datetime.datetime.now()
        self.tweets = []
        self.marker = []
        self.no_original = 0
        self.no_retweets = 0
        self.no_friends = 0
        self.no_followers = 0
        self.dataSetName =dataSetName
        self.timestamp = datetime.datetime.now()

        self.timeZone = None
        self.location = ""

    def add_tweet(self, s):

        entry = {"dt": s.get_created_at(),"text": s.get_text().replace("\n", "")}
        if s.get_retweet_status() is not None:
            entry["retweet_author"] = s.get_retweet_status().get_user(True).get_name()
        else:
            entry["retweet_author"] = ""

        self.tweets.append(entry)

        coordinates = s.get_coordinates()
        if coordinates is not None:
            print coordinates.item.item
            if coordinates.get_latitude() is not None and coordinates.get_longitude() is not None:
                self.marker.append({"position":{"lat": coordinates.get_latitude(),
                                                "lng": coordinates.get_longitude()},
                                    "title":s.get_created_at().strftime("%c")})