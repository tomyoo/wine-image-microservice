from wine_info.extensions import schemas


class AttributeSchema(schemas.Schema):
    body = schemas.Integer()
    fruit = schemas.Integer()
    earth = schemas.Integer(allow_none=True)
    tannin = schemas.Integer(allow_none=True)
    oak = schemas.Integer(allow_none=True)
    acidity = schemas.Integer(allow_none=True)


class ImageUrlsSchema(schemas.Schema):
    bottle = schemas.String(allow_none=True)
    label = schemas.String(allow_none=True)
    bottle_thumb = schemas.String(allow_none=True)


class VarietySchema(schemas.Schema):
    name = schemas.String()
    type = schemas.String()


class ClassificationSchema(schemas.Schema):
    name = schemas.String()
    type = schemas.String()


class WineSchema(schemas.Schema):
    name = schemas.String()
    brand = schemas.String()
    variety = schemas.Nested(VarietySchema)
    classification = schemas.Nested(ClassificationSchema)


class VintageSchema(schemas.Schema):
    id = schemas.Integer()
    year = schemas.Integer()
    short_tasting_note = schemas.String()
    tasting_note = schemas.String()
    abv = schemas.Float()
    attributes = schemas.Nested(AttributeSchema)
    region = schemas.List(schemas.String)
    grapes = schemas.List(schemas.String)
    tastes = schemas.List(schemas.String)
    pairings = schemas.List(schemas.String)
    traits = schemas.List(schemas.String)
    wine = schemas.Nested(WineSchema)
    brand = schemas.String()
    classification = schemas.String()
    image_urls = schemas.Nested(ImageUrlsSchema)
