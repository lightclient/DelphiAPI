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


class StakeEndpoint(object):
    """
    Endpoint that handles GET requests at: /stake/{address}

    Parameters:
        address

    Returns:
        JSON structure to client of the stake with address: address
    """
    def on_get(self, req, resp, address):

        #entry point for stake data
        stake_info = session.query(Stake).get(to_checksum_address(address))

        if(stake_info is None):
            raise falcon.HTTPNotFound(description="Could not find a stake with address {}".format(address))

        resp.body = json.objToJSON(stake_info, ['stakes'])


class ClaimantEndpoint(object):
    """
    Endpoint that handles GET requests at: /claimant/{address}, and returns
    information about stakes the claimant is involved with.

    Parameters:
        address

    Returns:
        JSON structure containing an array of stakes with claimant = address
    """
    def on_get(self, req, resp, address):

        claims_info = session.query(Claim).filter_by(claimant=to_checksum_address(address)).all()
        resp.body = json.listToJSON(claims_info, [])


class StakerEndpoint(object):
    """
    Endpoint that handles GET requests at: /staker/{address}, and returns
    information about stakes the staker has created.

    Parameters:
        address

    Returns:
        JSON structure containing an array of stakes with staker = address
    """
    def on_get(self, req, resp, address):

        stakes_info = session.query(Stake).filter_by(staker=to_checksum_address(address)).all()
        resp.body = json.listToJSON(stakes_info, ['stakes'])


class WhitelisteeEndpoint(object):
    """
    Endpoint that handles GET requests at: /whitelistee/{address}, and returns
    information about stakes the whitelistee is whitelisted on.

    Parameters:
        address

    Returns:
        JSON structure containing an array of stakes with whitelist = address
    """
    def on_get(self, req, resp, address):

        whitelists_info = session.query(Stake).filter(Stake.whitelist.any(claimant=to_checksum_address(address))).all()
        resp.body = json.listToJSON(whitelists_info, ['stakes'])


class ArbiterEndpoint(object):
    """
    Endpoint that handles GET requests at: /arbiter/{address}, and returns
    information about stakes the arbiter is arbiting on.

    Parameters:
        address

    Returns:
        JSON structure containing an array of stakes with arbiter = address
    """
    def on_get(self, req, resp, address):

        claims_info = session.query(Claim).filter_by(arbiter=to_checksum_address(address)).all()
        resp.body = json.listToJSON(claims_info, [])
