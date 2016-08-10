from dateutil import parser


class Status(object):
    T4J = dict(hashtags="hashtagEntities", mentions="userMentionEntities", user="user", text="text",
               created_at="createdAt", id="id", retweeted_status="retweetedStatus", language="lang", ISO_date=
               "createdAt", coordinates="geoLocation")

    RAW = dict(hashtags="entities.hashtags", mentions="entities.user_mentions", user="user", text="text",
               created_at="ISO_created_at", id="id", retweeted_status="retweeted_status", language="lang", ISO_date=
               "ISO_created_at", coordinates="coordinates.coordinates")

    GNIP = dict(hashtags="entities-hashtags", mentions="entities-user_mentions", text="clean-text",
                created_at="ISO_created_at", id="id", retweeted_status="retweeted_status", language="language",
                ISO_date=
                "ISO_created_at", user=["user-id", "user-utcOffset", "user-friendsCount", "user-name",
                                        "user-twitterTimeZone",
                                        "user-followersCount", "language"])

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

    def get_mentions(self):
        mention_list = self.get("mentions")
        return [UserMention(json, self.SCHEMA_ID) for json in mention_list]

    def get_user(self):
        return User(self.get("user"), self.SCHEMA_ID)

    def get_text(self):
        return self.get("text")

    def get_created_at(self):
        return self.get("created_at")
        # TwitterDate(self.get("created_at"), self.SCHEMA_ID).get_date_time()

    def get_id(self):
        return self.get("id")

    def get_retweet_status(self):
        try:
            return Status(self.get("retweeted_status"), self.SCHEMA_ID)
        except KeyError:
            return None

    def get_coordinates(self):
        try:
            return GeoLocation(self.get("coordinates"), self.SCHEMA_ID)
        except KeyError:
            return None


class GeoLocation(object):
    T4J = dict(longitude="longitude", latitude="latitude")
    RAW = dict(longitude=0, latitude=1)

    SCHEMA_MAP = {
        "T4J": T4J,
        "RAW": RAW
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


# def conv_dt(raw):
#     return raw
#
#
# def conv_json_dt(raw):
#     return parser.parse(raw)
#
# class TwitterDate(object):
#     SCHEMA_MAP = {
#         "T4J": conv_dt,
#         "RAW": conv_json_dt
#     }
#
#     def __init__(self, raw, schema_id):
#         self.SCHEMA_ID = schema_id
#         self.raw = raw
#
#     def get_date_time(self):
#         return self.SCHEMA_MAP[self.SCHEMA_ID](self.raw)


class User(object):
    T4J = dict(id="id", name="screenName", follower_count="followersCount", friends_count="friendsCount", lang="lang",
               utc_offset="utcOffset", time_zone="timeZone")
    RAW = dict(id="id", name="screen_name", follower_count="followers_count", friends_count="friends_count",
               lang="lang", utc_offset="utc_offset", time_zone="time_zone")
    GNIP = dict(id="user-id", name="user-name", follower_count="user-followersCount", friends_count="user-friendsCount",
                utc_offset="user-utcOffset", time_zone="user-twitterTimeZone", lang="language")

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

    def get_name(self):
        return self.get("name")

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
            return self.__getitem__(item)

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
