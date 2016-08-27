from dateutil import parser
import datetime

class Status(object):
    T4J = dict(hashtags="hashtagEntities", mentions="userMentionEntities", user="user", text="text",
               created_at="createdAt", id="id", retweeted_status="retweetedStatus", language="lang", ISO_date=
               "createdAt", coordinates="geoLocation", user_sub_field="user", retweet_user="user",
               retweeted_status_exists="retweetedStatus.text",n_retweeted="retweetCount")

    RAW = dict(hashtags="entities.hashtags", mentions="entities.user_mentions", user="user", text="text",
               created_at="ISO_created_at", id="id", retweeted_status="retweeted_status", language="lang", ISO_date=
               "ISO_created_at", coordinates="coordinates.coordinates", user_sub_field="user", retweet_user="user",
               retweeted_status_exists="retweeted_status.text",n_retweeted="retweet_count")

    GNIP = dict(hashtags="entities-hashtags", mentions="entities-user_mentions", text="clean-text",
                created_at="ISO_created_at", id="id", retweeted_status="retweeted_status", language="language",
                ISO_date=
                "ISO_created_at", user_sub_field=["user-id", "user-utcOffset", "user-friendsCount", "user-screen_name",
                                                  "user-twitterTimeZone", "user-followersCount","language",
                                                  "user-location","user-summary","user-image", "user-name",
                                                  "user-postedTime"], user="",
                retweet_user="user", retweeted_status_exists="retweeted_status.text",n_retweeted="retweetCount",
                coordinates="entities-user-place-coordinates")

    SCHEMA_MAP = {
        "T4J": T4J,
        "RAW": RAW,
        "GNIP": GNIP
    }

    def __init__(self, json, schema_id):
        self.item = DictionaryWrapper(json)
        self.SCHEMA = self.SCHEMA_MAP[schema_id]
        self.SCHEMA_ID = schema_id

    def get(self, key):
        return self.item.get(self.SCHEMA[key])

    def get_hashtags(self):
        hashtag_list = self.get("hashtags")
        return [h_tag["text"] for h_tag in hashtag_list]

    def get_n_retweeted(self):
        return self.get("n_retweeted")

    def get_mentions(self):
        mention_list = self.get("mentions")
        return [UserMention(json, self.SCHEMA_ID) for json in mention_list]

    def get_user(self, retweet=False):
        if retweet:
            return User(self.get("retweet_user"), self.SCHEMA_ID, True)
        return User(self.get("user_sub_field"), self.SCHEMA_ID)

    def get_text(self):
        return self.get("text")

    def get_created_at(self):
        return self.get("created_at")

    def get_id(self):
        return self.get("id")

    def get_retweet_status(self):
        try:
            if self.get("retweeted_status_exists") is None:
                return None
            return Status(self.get("retweeted_status"), self.SCHEMA_ID)
        except KeyError:
            return None

    def get_coordinates(self):
        try:
            if self.get("coordinates") is not None:
                return GeoLocation(self.get("coordinates"), self.SCHEMA_ID)
        except KeyError:
            return None


class GeoLocation(object):
    T4J = dict(longitude="longitude", latitude="latitude")
    RAW = dict(longitude=0, latitude=1)
    GNIP = dict(longitude="lon", latitude="lat")

    SCHEMA_MAP = {
        "T4J": T4J,
        "RAW": RAW,
        "GNIP": GNIP
    }

    def __init__(self, json, schema_id):
        self.item = DictionaryWrapper(json)
        self.SCHEMA = self.SCHEMA_MAP[schema_id]
        self.SCHEMA_ID = schema_id

    def get(self, key):
        return self.item.get(self.SCHEMA[key])

    def get_latitude(self):
        return self.get("latitude")

    def get_longitude(self):
        return self.get("longitude")

    def __str__(self):
        return str(self.get_longitude()) + "," + str(self.get_latitude())


class User(object):
    T4J = dict(id="id", name="screenName", follower_count="followersCount", friends_count="friendsCount", lang="lang",
               utc_offset="utcOffset", time_zone="timeZone", retweet_screen_name = "screenName",
               image_url="originalProfileImageURL", created_at = "createdAt",
               real_name="name", location="location", description = "description")
    RAW = dict(id="id", name="screen_name", follower_count="followers_count", friends_count="friends_count",
               lang="lang", utc_offset="utc_offset", time_zone="time_zone", retweet_screen_name="screen_name",
               image_url="profile_image_url",real_name="name", location="location", description = "description",
               created_at="created_at")
    GNIP = dict(id="user-id", name="user-screen_name", follower_count="user-followersCount", friends_count="user-friendsCount",
                utc_offset="user-utcOffset", time_zone="user-twitterTimeZone", lang="language", retweet_screen_name =
                "screen_name",image_url="user-image",real_name="user-name", location="user-location", description =
                "user-summary", created_at = "user-postedTime")
    RTWT_GNIP = dict(name="screen_name", real_name="name")

    SCHEMA_MAP = {
        "T4J": T4J,
        "RAW": RAW,
        "GNIP": GNIP
    }

    RETWEET_SCHEMA_MAP = {
        "T4J": T4J,
        "RAW": RAW,
        "GNIP": RTWT_GNIP
    }

    def __init__(self, json, schema_id, retweet=False):
        self.item = DictionaryWrapper(json)
        if retweet:
            self.SCHEMA = self.RETWEET_SCHEMA_MAP[schema_id]
        else:
            self.SCHEMA = self.SCHEMA_MAP[schema_id]
        self.SCHEMA_ID = schema_id

    def get(self, key):
        return self.item.get(self.SCHEMA[key])

    def get_image_url(self):
        return self.get("image_url")

    def get_name(self):
        return self.get("name")

    def get_real_name(self):
        return self.get("real_name")

    def get_id(self):
        return self.get("id")

    def get_follower_count(self):
        return self.get("follower_count")

    def get_friends_count(self):
        return self.get("friends_count")

    def get_lang(self):
        return self.get("lang")

    def get_time_zone(self):
        return self.get("time_zone")

    def get_utc_offset(self):
        return self.get("utc_offset")

    def get_location(self):
        return self.get("location")

    def get_description(self):
        return self.get("description")

    def get_profile_creation_date(self):
        date = self.get("created_at")
        if isinstance(date, datetime.datetime):
            return date
        else:
            return parser.parse(date)

class UserMention(object):
    T4J = dict(id="id", name="screenName")
    RAW = dict(id="id", name="screen_name")
    GNIP = dict(id="id", name="screen_name")
    SCHEMA_MAP = {
        "T4J": T4J,
        "RAW": RAW,
        "GNIP": GNIP,
    }

    def __init__(self, json, schema_id):
        self.item = DictionaryWrapper(json)
        self.SCHEMA = self.SCHEMA_MAP[schema_id]
        self.SCHEMA_ID = schema_id

    def get(self, key):
        return self.item.get(self.SCHEMA[key])

    def get_user_id(self):
        return self.get("id")

    def get_name(self):
        return self.get_user_name()

    def get_id(self):
        return self.get_user_id()

    def get_user_name(self):
        return self.item.get(self.SCHEMA["name"])


class DictionaryWrapper(object):
    def __init__(self, json):
        self.item = json

    def get(self, item):
        if isinstance(item, list):
            return {i: self.__getitem__(i) if i in self.item else None for i in item}
        else:
            try:
                return self.__getitem__(item)
            except KeyError:
                return None

    def put(self, key, value):
        return self.__setitem__(key, value)

    def __getitem__(self, item):

        return DictionaryWrapper.rec_get(self.item, item)

    def __setitem__(self, key, value):

        return DictionaryWrapper.rec_put(self.item, key, value)

    @staticmethod
    def rec_put(d, keys, item):
        if "." in keys:
            key, rest = keys.split(".", 1)
            if key not in d:
                d[key] = {}
            DictionaryWrapper.rec_put(d[key], rest, item)
        else:
            d[keys] = item

    @staticmethod
    def rec_get(d, keys):
        if "." in keys:
            key, rest = keys.split(".", 1)
            return DictionaryWrapper.rec_get(d[key], rest)
        else:
            return d[keys]


if __name__ == "__main__":
    print Status({"user-id": 123, "user-name": "cps"}, "GNIP").get_user().item.item
