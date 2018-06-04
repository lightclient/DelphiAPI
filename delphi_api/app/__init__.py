import falcon
import logging
import os

from falcon_cors import CORS

from app.migrations.migrate import migrate
from app.middleware import CrossDomain, JSONTranslator
from app.util.logging import setup_logging
from app.util.error import error_handler
from app.util.connection import connect

from app.resources.root import RootResources, RootNameResources

from app.resources.endpoints import StakeEndpoint, StakerEndpoint, ClaimantEndpoint, WhitelisteeEndpoint, ArbiterEndpoint

logger = logging.getLogger(__name__)


def create_app():
    setup_logging()

    # cors = CORS(allow_origins_list=['http://test.com:8080'])
    cors = CORS(allow_all_origins=True)

    app = falcon.API(
        middleware=[
            # CrossDomain(),
            # JSONTranslator()
            cors.middleware
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

# create endpoints
def _setup_routes(app):
    app.add_route("/", RootResources())

    #WhitelisteeEndpoint defined in app.resources.arbiter.py
    app.add_route("/arbiter/{address}", ArbiterEndpoint())

    # StakeEndpoint defined in app.resources.stake.py
    app.add_route("/stake/{address}", StakeEndpoint())

    #StakerEndpoint defined in app.resources.staker.py
    app.add_route("/staker/{address}", StakerEndpoint())

    #ClaimantEndpoint defined in app.resources.claimant.py
    app.add_route("/claimant/{address}", ClaimantEndpoint())

    #WhitelisteeEndpoint defined in app.resources.whitelistee.py
    app.add_route("/whitelistee/{address}", WhitelisteeEndpoint())

    



# entry point for python code
app = create_app()
