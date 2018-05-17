from decimal import Decimal
import sys
sys.path.append('/usr/src/app')

from app.migrations.models import Base, Stake, Whitelistee
from app.util.connection import connect
from sqlalchemy.orm import sessionmaker
from app.event_processor.main import event_processor, session, engine
from app.event_processor.test.payloads import *

Base.metadata.reflect(bind=engine)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def test_stake_saved_in_database():
    event_processor(stakeCreated)
    stake = session.query(Stake).filter_by(address=stakeCreated.get('address')).first()
    assert stake.staker == stakeCreated.get('sender')
    assert stake.claimable_stake == int(Decimal(stakeCreated.get('params').get('value')))
    assert stake.data == stakeCreated.get('params').get('data')

def test_whitelistee_is_associated_with_stake():
    event_processor(claimantWhitelisted)
    stake = session.query(Stake).filter_by(address=claimantWhitelisted.get('address')).first()
    assert stake.whitelist[0].claimant == claimantWhitelisted.get('params').get('claimant')

def test_stake_release_time_increased():
    event_processor(releaseTimeIncreased)
    stake = session.query(Stake).filter_by(address=claimantWhitelisted.get('address')).first()
    assert stake.claim_deadline == int(Decimal( releaseTimeIncreased.get('params').get('stakeReleaseTime') ))

Base.metadata.reflect(bind=engine) # need to figure out what this does
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
