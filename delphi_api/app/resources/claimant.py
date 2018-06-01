import app.util.json as json

import falcon
from app.migrations.models import Stake, Whitelistee, Token, Claim, Arbiter
from app.util.connection import connect
from sqlalchemy.orm import sessionmaker

from decimal import Decimal

engine = connect()
Session = sessionmaker(bind=engine)
session = Session()

class ClaimantEndpoint(object):
    def on_get(self, req, resp, address):                                              
        claims_info = session.query(Claim).filter_by(claimant=address).all()                 
        resp.body = json.listToJSON(claims_info, [])
