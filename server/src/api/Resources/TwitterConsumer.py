from api.Auth import Resource
from flask_restful import marshal_with, fields, abort

twitter_consumer_meta = {
    "id": fields.Integer(attribute="id"),
    "pid": fields.Integer,
    "alive": fields.Boolean,
    "uri_base": fields.Url("twitterConsumer")
}


class TwitterConsumerMeta(object):
    def __init__(self, id, pid, alive):
        self.id = id
        self.alive = alive
        self.pid = pid


class TwitterConsumerList(Resource):
    def __init__(self, **kwargs):
        self.twitter_service = kwargs["twitter_service"]

    @marshal_with(twitter_consumer_meta)
    def post(self):
        consumer_id, c = self.twitter_service.router.spin_up()

        return TwitterConsumerMeta(consumer_id, c.ident, c.is_alive())

    @marshal_with(twitter_consumer_meta)
    def get(self):
        consumers = []

        for c_key in self.twitter_service.router.routers.keys():
            _, c = self.twitter_service.router.routers[c_key]
            consumers.append(TwitterConsumerMeta(c_key, c.ident, c.is_alive()))

        return consumers


class TwitterConsumer(Resource):
    def __init__(self, **kwargs):
        self.twitter_service = kwargs["twitter_service"]

    @marshal_with(twitter_consumer_meta)
    def get(self, id):

        try:
            _, c = self.twitter_service.router.routers[id]
            return TwitterConsumerMeta(id, c.ident, c.is_alive())
        except KeyError:
            abort(404, message="Consumer {} does not exist".format(id))

    def delete(self, consumer_id):

        self.twitter_service.router.spin_down(int(consumer_id))

        return "", 204
