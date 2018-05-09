import app.util.json as json

import app.util.json as json
import falcon
from app.migrations.models import Stake, Whitelistee
from app.util.connection import connect
from sqlalchemy.orm import sessionmaker

from decimal import Decimal

engine = connect()

Session = sessionmaker(bind=engine)
session = Session()

class StakeEndpoint(object):
    def on_get(self, req, resp, address):

        stake = session.query(Stake).filter_by(address=address).first()
        whitelist = [ el.claimant for el in stake.whitelist ]

        resp.body = json.dumps({
            'data': {
                'staker': stake.staker,
                'value': stake.claimable_stake,
                'token': {
                    'name': 'DelphiCoin',
                    'symbol': 'DC',
                    'address': '0x5ed8cee6b63b1c6afce3ad7c92f4fd7e1b8fad9f'
                },
                'minimum_fee': stake.minimum_fee,
                'data': stake.data,
                'claim_deadline': str( int(Decimal(stake.claim_deadline.real)) ),
                'arbiter': {
                    'name': '',
                    'description': '',
                    'address': '0x498bad589c7acd871945ed6ca30b7bab0a977af7'
                },
                'whitelisted_claimants': whitelist,
                'claims': [
                    {
                      "id": 0,
                      "amount": 25,
                      "fee": 5,
                      "surplus_fee": 0,
                      "data": "QmT4AeWE9Q9EaoyLJiqaZuYQ8mJeq4ZBncjjFH9dQ9uDVA",
                      "ruling": 0,
                      "ruled": 0,
                      "settlement_failed": 1
                    }
                ],
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
