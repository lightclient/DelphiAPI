import falcon
import logging
import os

from app.migrations.migrate import migrate
from app.middleware import CrossDomain, JSONTranslator
from app.util.logging import setup_logging
from app.util.error import error_handler
from app.util.connection import connect

from app.resources.root import RootResources, RootNameResources
from app.resources.stake import StakeEndpoint


logger = logging.getLogger(__name__)


def create_app():
    setup_logging()

    app = falcon.API(
        middleware=[
            # CrossDomain(),
            # JSONTranslator()
        ],
    )

    app.add_error_handler(Exception, error_handler)

    # if this is the dev environment, clear the database when booted up
    if os.environ['ENV'] == 'DEV':
        engine = create_table()
        migrate(engine)

    _setup_routes(app)

    return app

def create_table():
    return connect()


def start():
    logger.info("Environment: {}".format(settings.get("ENV_NAME")))

#create endpoints
def _setup_routes(app):
    app.add_route("/", RootResources())

    #StakeEndpoint defined in app.resources.stake.py
    app.add_route("/stake/{address}", StakeEndpoint())

#entry point for python code
app = create_app()
