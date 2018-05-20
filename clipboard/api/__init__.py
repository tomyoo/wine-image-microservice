from wine_info.extensions import schemas, statsd
#from .logging import setup_logging
from .handlers import setup_handlers
from ..app_factory import create_app as factory_create_app


def create_app(settings_override=None):
    """Returns an api application instance"""
    extensions = frozenset([statsd, schemas])

    app = factory_create_app(__name__, __path__, settings_override, extensions)

    if not app.extensions:
        app.extensions = {}
    app.extensions['statsd'] = statsd

    #setup_logging(app)
    setup_handlers(app)

    return app
