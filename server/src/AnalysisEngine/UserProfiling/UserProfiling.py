import json
import logging
from collections import OrderedDict
import datetime
from dateutil import parser
from AnalysisEngine.Analysis import Analysis
from AnalysisEngine.TwitterObj import Status, User
from AnalysisEngine import Util
from AnalysisEngine.UserProfiling.UserProfile import UserProfile

class UserProfiling(Analysis):
    _logger = logging.getLogger(__name__)
    __arguments = [dict(name="user_screen_name", prettyName="User Screen Name", type="string",
                        default="iVoteLeave"),
                   dict(name="Limit", prettyName="Tweet Limit", type="integer",
                         default=1000)]

    def __init__(self, analytics_meta):
        super(UserProfiling, self).__init__(analytics_meta)

    @classmethod
    def get_classification(cls):
        return "User"

    @classmethod
    def get_type(cls):
        return "Profile"

    @classmethod
    def get_prefered_vis(cls):
        return "url_html", "StaticHTML"

    @classmethod
    def get_args(cls):
        return cls.__arguments + super(UserProfiling, cls).get_args()

    def process(self):

        user_screen_name = self.args["user_screen_name"]
        limit = self.args["Limit"]
        user_name_key = Util.join_keys(Status.SCHEMA_MAP[self.schema]["user"],
                                              User.SCHEMA_MAP[self.schema]["name"])

        query = self.get_time_bounded_query({user_name_key: user_screen_name})
        cursor = self.get_sorted_cursor(query, limit, reverse=True)

        user_profile = UserProfile(user_screen_name, self.dataset_meta.description)

        n_retweets = 0
        n_original = 0
        first = True
        self._logger.info("Beginning profiling")

        for c in cursor:
            s = Status(c, self.schema)
            if first:
                user = s.get_user()
                user_profile.no_followers =  user.get_follower_count()
                user_profile.no_friends = user.get_friends_count()
                user_profile.timestamp = s.get_created_at()
                user_profile.name = user.get_real_name()
                user_profile.profileImage = user.get_image_url().replace("_normal","")
                user_profile.timeZone = user.get_time_zone()
                user_profile.location = user.get_location()
                first = False
            if s.get_retweet_status() is None:
                n_original += 1
            else:
                n_retweets += 1
            user_profile.add_tweet(s)

        user_profile.no_retweets = n_retweets
        user_profile.no_original = n_original
        self._logger.info("Finished profiling")

        self.export_html(user_profile, export_type="userProfile")
        self.export_json(user_profile.__dict__)

        return True
