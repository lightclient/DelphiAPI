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
        stake_info = session.query(Stake).filter_by(address=address).first() #can you not use query(Stake).get(address)? since the address is the primary key?

        #internal relationships (1 to many)
        whitelist_info = [ el.claimant for el in stake_info.whitelist ]
        claims_info = [
            {'claimant': el.claimant,
             'arbiter' : el.arbiter,
             'surplus_fee': el.surplus_fee,
             'data': el.data,
             'ruling': el.ruling,
             'ruled': el.ruled,
             'settlement_failed': el.settlement_failed
            }
            for el in stake_info.claims ]

        #foreign tables (1 to 1)
        # token_info = session.query(Token).filter_by(address=stake_info.token).first()
        # arbiter_info = session.query(Arbiter).filter_by(address=stake_info.arbiter).first()

        #TODO: de-hard-code settlements once it is implemented for the DB

        resp.body = json.dumps({
            'data': {
                'staker': stake_info.staker,
                'value': stake_info.claimable_stake,
                'token': {
                    'name': stake_info.token.name,
                    'symbol': stake_info.token.symbol,
                    'address': stake_info.token.address
                },
                'minimum_fee': stake_info.minimum_fee,
                'data': stake_info.data,
                'claim_deadline': str( int(Decimal(stake_info.claim_deadline.real)) ),
                'arbiter': {
                    'name': stake_info.arbiter.name,
                    'description': stake_info.arbiter.description,
                    'address': stake_info.arbiter.address
                },
                'whitelisted_claimants': whitelist_info,
                'claims': claims_info,
                'settlements': [
                    {
                      "amount": 10,
                      "staker_agrees": 0,
                      "claimant_agrees": 0
                    }
                ]
            },
            'errors': []
        })
