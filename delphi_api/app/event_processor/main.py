import json
import time
from datetime import datetime, timedelta
import ast

import sys
sys.path.append('/usr/src/app')

from app.migrations.models import Stake, Whitelistee, Claim, Token, Arbiter
from app.util.connection import connect
from sqlalchemy.orm import sessionmaker
from app.util.logging import pretty_print

from app.event_processor.rabbitmq import client
from app.event_processor.helpers import sanitize

engine = connect()

Session = sessionmaker(bind=engine)
session = Session()

def message_handler(ch, method, properties, body):

    # converts body from a byte string to a dictionary
    event = json.loads(body.decode())

    event_processor(event)

    # pretty_print(event)

    ch.basic_ack(delivery_tag = method.delivery_tag)

def event_processor(event):

    # break the paramaters out into a more accessible form
    params = event.get('params') # the params passed directly to the smart contract
    values = event.get('values') # the values emitted from the event

    #################
    # STAKE CREATED #
    #################
    if event.get('type') == 'StakeCreated':
        token = session.query(Token).filter_by(address=params.get('token')).first()
        arbiter = session.query(Arbiter).filter_by(address=params.get('arbiter')).first()

        if token == None:
            token = Token(
                address=params.get('token'),
                name=event.get('token').get('name'),
                symbol=event.get('token').get('symbol'),
                decimals=event.get('token').get('decimals')
            )

        if arbiter == None:
            arbiter = Arbiter(address=params.get('arbiter'))

        stake = Stake(
            address=values.get('_contractAddress'),
            staker=event.get('sender'),
            token=token,
            claimable_stake=sanitize( params.get('value') ),
            data=params.get('data'),
            arbiter=arbiter,
            minimum_fee=sanitize( params.get('minimumFee') ),
            claim_deadline=sanitize( params.get('stakeReleaseTime') )
        )

        session.add_all([stake,token,arbiter])

    ########################
    # CLAIMANT WHITELISTED #
    ########################
    if event.get('type') == 'ClaimantWhitelisted':
        whitelistee = Whitelistee(
            stake=event.get('address'),
            claimant=params.get('claimant'),
            deadline=sanitize( params.get('deadline') )
        )

        stake = session.query(Stake).filter_by(address=event.get('address')).first()
        stake.whitelist.append(whitelistee)

        session.add_all([stake, whitelistee])

    ################
    # CLAIM OPENED #
    ################
    # TODO: write tests
    # TODO: handle case where a claim is opened w/o settlement
    if event.get('type') == 'ClaimOpened':
        claim = Claim(
            stake=event.get('address'),
            id=sanitize( values.get('_claimId') ),
            claimant=params.get('claimant'),
            amount=sanitize( params.get('amount') ),
            arbiter=params.get('arbiter'),
            fee=sanitize( params.get('fee') ),
            surplus_fee=0,
            data=params.get('data'),
            ruling=0,
            ruled=False,
            settlements=False
        )

        stake = session.query(Stake).filter_by(address=event.get('address')).first()

        stake.claimable_stake -= claim.amount + claim.fee
        stake.claims.append(claim)

        session.add_all([stake, claim])

    #################
    # FEE INCREASED #
    #################
    # TODO: write tests
    # TODO: figure out how we're gonna get claim id
    if event.get('type') == 'FeeIncreased':
        claim = session.query(Claim).filter_by(
            stake=event.get('address'),
            id=params.get('_claimId'),
        ).first()

        claim.surplus_fee += sanitize( params.get('_amount') )

        session.add(claim)

    ###################
    # STAKE INCREASED #
    ###################
    #TODO: write test
    if event.get('type') == 'StakeIncreased':
        stake = session.query(Stake).filter_by(address=event.get('address')).first()

        stake.claimable_stake += sanitize( params.get('value') )

        session.add(stake)

    if event.get('type') == 'ReleaseTimeIncreased':
        stake = session.query(Stake).filter_by(address=event.get('address')).first()

        stake.claim_deadline = sanitize( params.get('stakeReleaseTime') )

        session.add(stake)

    ###################
    # STAKE WITHDRAWN #
    ###################
    # TODO: write test
    if event.get('type') == 'StakeWithdrawn':
        stake = session.query(Stake).filter_by(address=event.get('address')).first()

        stake.claimable_stake = 0

        session.add(stake)

    # commit the changes to the database
    session.commit()


if __name__ == "__main__":
    client.basic_consume(message_handler, queue='delphi_events')
    client.start_consuming()
