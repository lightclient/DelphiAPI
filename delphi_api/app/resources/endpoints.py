import app.util.json as json
import falcon
from app.migrations.models import Stake, Whitelistee, Token, Claim, Arbiter
from app.util.connection import connect
from sqlalchemy.orm import sessionmaker
from eth_utils import to_checksum_address
from decimal import Decimal

engine = connect()

Session = sessionmaker(bind=engine)
session = Session()

#TODO: refactor to_checksum_address function to elsewhere to reduce repeat code

#/stake/{address}
class StakeEndpoint(object):
    def on_get(self, req, resp, address):


        #entry point for stake data
        stake_info = session.query(Stake).get(to_checksum_address(address))

        if(stake_info is None):
            raise falcon.HTTPNotFound(description="Could not find a stake with address {}".format(address))

        resp.body = stake_info.toJSON()


#/claimant/{address}
class ClaimantEndpoint(object):
    def on_get(self, req, resp, address):

        claims_info = session.query(Claim).filter_by(claimant=to_checksum_address(address)).all()
        resp.body = json.listToJSON(claims_info, [])


#/staker/{address}
class StakerEndpoint(object):
    def on_get(self, req, resp, address):

        stakes_info = session.query(Stake).filter_by(staker=to_checksum_address(address)).all()
        resp.body = json.listToJSON(stakes_info, ['stakes'])


#/whitelistee/{address}
class WhitelisteeEndpoint(object):
    def on_get(self, req, resp, address):

        whitelists_info = session.query(Stake).filter(Stake.whitelist.any(claimant=to_checksum_address(address))).all()
        resp.body = json.listToJSON(whitelists_info, ['stakes'])


#/arbiter/{address}
class ArbiterEndpoint(object):
    def on_get(self, req, resp, address):

        claims_info = session.query(Claim).filter_by(arbiter=to_checksum_address(address)).all()
        resp.body = json.listToJSON(claims_info, [])
