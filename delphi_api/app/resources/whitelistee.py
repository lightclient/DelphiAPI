import app.util.json as json

import falcon
from app.migrations.models import Stake, Whitelistee, Token, Claim, Arbiter
from app.util.connection import connect
from sqlalchemy.orm import sessionmaker

from decimal import Decimal

engine = connect()
Session = sessionmaker(bind=engine)
session = Session()

class WhitelisteeEndpoint(object):
    def on_get(self, req, resp, address):
        whitelists_info = session.query(Stake).filter(Stake.whitelist.any(claimant=address)).all()
        resp.body = json.listToJSON(whitelists_info, ['stakes'])
