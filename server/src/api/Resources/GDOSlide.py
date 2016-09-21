import logging
import uuid

from flask_restful import reqparse, marshal_with, fields, abort
from mongoengine.queryset import DoesNotExist

from api.Auth import Resource
from api.Objects.MetaData import Slides, DictionaryWrap

slide_fields = {
    "description": fields.String,
    "sections": DictionaryWrap(attribute="sections"),
    "id": fields.String
}


class SlideList(Resource):
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('description', type=str, help="Slide description")
        self.parser.add_argument('sections', type=dict, action="append", help="Section")

    @marshal_with(slide_fields)
    def get(self):
        return [i._data for i in Slides.objects()]

    @marshal_with(slide_fields)
    def post(self):
        args = self.parser.parse_args()
        # print args
        slide = Slides(description=args["description"],
                       id=str(uuid.uuid4()),
                       sections=args["sections"])

        slide.save()
        return slide

class Slide(Resource):
    logging = logging.getLogger(__name__)

    def delete(self, id):

        try:
            found = Slides.objects.get(id=id)
            found.delete()
            return "", 204
        except DoesNotExist:
            abort(404, message="Slide {} does not exist".format(id))
            return
