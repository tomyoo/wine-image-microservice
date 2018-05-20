from flask_statsd import StatsD
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

schemas = Marshmallow()

db = SQLAlchemy()

statsd = StatsD()
