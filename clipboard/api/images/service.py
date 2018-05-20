from ..exceptions import ApiException

from ...extensions import db
from ...models.images import Image


def get_image_by_id(image_id):
    try:
        image = Image.query.filter(db.and_(
            Image.id == image_id)).first()
    except AttributeError:
        raise ApiException("No image with that ID found.")

    return image
