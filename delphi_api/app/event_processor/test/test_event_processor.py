from decimal import Decimal
import sys
sys.path.append('/usr/src/app')

from app.migrations.models import Base, Stake, Whitelistee, Token, Arbiter
from app.util.connection import connect
from sqlalchemy.orm import sessionmaker
from app.event_processor.main import event_processor, session, engine
from app.event_processor.test.payloads import *

Base.metadata.reflect(bind=engine)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def test_stake_saved_in_database():
    event_processor(stakeCreated)
    stake = session.query(Stake).filter_by(address=stakeCreated.get('values').get('_contractAddress')).first()

    assert stake.staker == stakeCreated.get('sender')
    assert stake.claimable_stake == int(Decimal(stakeCreated.get('params').get('value')))
    assert stake.data == stakeCreated.get('params').get('data')

    # make sure token is created correctly
    assert stake.token_id == stakeCreated.get('params').get('token')
    assert stake.token.address == stakeCreated.get('params').get('token')
    token = session.query(Token).filter_by(address=stake.token.address).first()
    assert token.address == stakeCreated.get('params').get('token')

    # make sure arbiter is created correctly
    assert stake.arbiter_id == stakeCreated.get('params').get('arbiter')
    assert stake.arbiter.address == stakeCreated.get('params').get('arbiter')
    arbiter = session.query(Arbiter).filter_by(address=stake.arbiter.address).first()
    assert arbiter.address == stakeCreated.get('params').get('arbiter')

def test_whitelistee_is_associated_with_stake():
    event_processor(claimantWhitelisted)
    stake = session.query(Stake).filter_by(address=claimantWhitelisted.get('address')).first()
    assert stake.whitelist[0].claimant == claimantWhitelisted.get('params').get('claimant')

def test_stake_release_time_increased():
    event_processor(releaseTimeIncreased)
    stake = session.query(Stake).filter_by(address=claimantWhitelisted.get('address')).first()
    assert stake.claim_deadline == int(Decimal( releaseTimeIncreased.get('params').get('stakeReleaseTime') ))

def test_multiple_stake_using_same_token():
    event_processor(stakeCreated2)
    stake = session.query(Stake).filter_by(address=stakeCreated2.get('values').get('_contractAddress')).first()

    assert stake.staker == stakeCreated2.get('sender')
    assert stake.claimable_stake == int(Decimal(stakeCreated2.get('params').get('value')))
    assert stake.data == stakeCreated2.get('params').get('data')

    # make sure token is created correctly
    assert stake.token_id == stakeCreated2.get('params').get('token')
    assert stake.token.address == stakeCreated2.get('params').get('token')
    token = session.query(Token).filter_by(address=stake.token.address).first()
    assert token.address == stakeCreated2.get('params').get('token')

    # make sure arbiter is created correctly
    assert stake.arbiter_id == stakeCreated2.get('params').get('arbiter')
    assert stake.arbiter.address == stakeCreated2.get('params').get('arbiter')
    arbiter = session.query(Arbiter).filter_by(address=stake.arbiter.address).first()
    assert arbiter.address == stakeCreated2.get('params').get('arbiter')

def test_open_claims_on_stake():
    stake = session.query(Stake).filter_by(address=stakeCreated.get('values').get('_contractAddress')).first()

    event_processor(claim1)

    assert len(stake.claims) == 1
    assert stake.claims[0].claimant == claim1.get('params').get('claimant')
    assert stake.claims[0].data == claim1.get('params').get('data')
    assert str(int(stake.claims[0].fee)) == claim1.get('params').get('fee')

    event_processor(claim2)

    assert len(stake.claims) == 2
    assert stake.claims[1].claimant == claim2.get('params').get('claimant')
    assert stake.claims[1].data == claim2.get('params').get('data')
    assert str(int(stake.claims[1].fee)) == claim2.get('params').get('fee')



Base.metadata.reflect(bind=engine) # need to figure out what this does
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
