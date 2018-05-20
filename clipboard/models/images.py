from ..extensions import db


class Variation(db.Model):
    __tablename__ = 'variations'

    id = db.Column(db.Integer, primary_key=True)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    name = db.Column(db.String)


class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    cdn_url = db.Column(db.String)
    created_on = db.Column(db.DateTime)

    variation_id = db.Column(db.Integer, db.ForeignKey('variations.id'))
    variation = db.relationship('Variation', foreign_keys=variation_id)

    variations = db.relationship('ImageVariation',
                                 foreign_keys=['parent_id'],
                                 backref='images_variations')


class ImageVariation(db.Model):
    __tablename__ = 'images_variations'

    image_id = db.Column(db.Integer, db.ForeignKey('images.id'))
    image = db.relationship('Image', foreign_keys=image_id)

    parent_id = db.Column(db.Integer, db.ForeignKey('images.id'))
    parent = db.relationship('Image', foreign_keys=parent_id)

    variation_id = db.Column(db.Integer, db.ForeignKey('variations.id'))
    variation = db.relationship('Variation', foreign_keys=variation_id)
