import app.util.json as json

import falcon
from app.migrations.models import Stake, Whitelistee, Token, Claim, Arbiter
from app.util.connection import connect
from sqlalchemy.orm import sessionmaker

from decimal import Decimal

engine = connect()

Session = sessionmaker(bind=engine)
session = Session()

class StakerEndpoint(object):
    def on_get(self, req, resp, address):

        #stakes = []

        #for stake in session.query(Stake).filter_by(staker=address):
        #    stakes.append(stake.toJSON())

        stakes_info = session.query(Stake).filter_by(staker=address).all()
        resp.body = json.listToJSON(stakes_info, ['stakes'])

        #resp.body = stakes
        #resp.body = json.dumps(stakes)
        #resp.body = json.dumps(stakes)
