import app.util.json as json

import falcon
from app.migrations.models import Stake, Whitelistee, Token, Claim, Arbiter
from app.util.connection import connect
from sqlalchemy.orm import sessionmaker

from decimal import Decimal

engine = connect()

Session = sessionmaker(bind=engine)
session = Session()

class StakeEndpoint(object):
    def on_get(self, req, resp, address):
        #entry point for stake data
        stake_info = session.query(Stake).get(address)
        if (stake_info is None):
            raise falcon.HTTPNotFound(description="Could not find a stake with address {}".format(address))
        else:
            resp.body = stake_info.toJSON()
