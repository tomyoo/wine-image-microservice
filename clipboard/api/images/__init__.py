import os
import json

from flask import Blueprint, request, current_app
from flask_restplus import Api, Resource

from ..common.failures import Failures
from ..exceptions import ApiException

from .schema import VintageSchema

from .service import get_image_by_id


# named Blueprint object, so as to be registered by the app factory
blueprint = Blueprint(
    'images', __name__, url_prefix='/images')
api = Api(blueprint)


variation = api.schema_model('Variation', {
    'required': ['id'],
    'properties': {
        'id': {
            'type': 'integer'
        },
        'name': {
            'type': 'string'
        },
        'width': {
            'type': 'integer'
        },
        'height': {
            'type': 'integer'
        }
    },
    'type': 'object'
})


image = api.schema_model('Image', {
    'required': ['id'],
    'properties': {
        'id': {
            'type': 'integer'
        },
        'variation': {
            '$ref': '#/definitions/Variation',
        },
        'created_on': {
            'type': 'string',
            'format': 'date-time'
        },
        'cdn_url': {
            'type': 'string'
        }
    },
    'type': 'object'
})


@api.route('/<image_id>')
class ImageResource(Resource):

    def get(self, image_id):
        """ Retrieve the information about an image """

        image_information = get_image_by_id(image_id)

        return image_information
