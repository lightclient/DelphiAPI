from decimal import Decimal
import sys
sys.path.append('/usr/src/app')

from app.migrations.models import Base, Stake, Whitelistee
from app.util.connection import connect
from sqlalchemy.orm import sessionmaker
from app.event_processor.main import event_processor, session, engine

Base.metadata.reflect(bind=engine)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

stakeCreated = {
    'transactionHash': '0xe9aabe3feaf9fa8759ce2f86d673036c59b9a182398ee3c8913e4b4dea2b3e9b',
    'block': 35,
    'type': 'StakeCreated',
    'address': '0x345cA3e014Aaf5dcA488057592ee47305D9B3e10',
    'sender': '0x627306090abaB3A6e1400e9345bC60c78a8BEf57',
    'params': {
         'value': '100',
         'token': '0x8f0483125fcb9aaaefa9209d8e9d7b9c8b9fb90f',
         'minimumFee': '10',
         'data': 'i love cats',
         'stakeReleaseTime': '9.999999999999999999999999999999999e+33',
         'arbiter': '0xbaaa2a3237035a2c7fa2a33c76b44a8c6fe18e87'
    }
}

claimantWhitelisted = {
    'transactionHash': '0xe9aabe3feaf9fa8759ce2f86d673036c59b9a182398ee3c8913e4b4dea2b3e9b',
    'block': 35,
    'type': 'ClaimantWhitelisted',
    'address': '0x345cA3e014Aaf5dcA488057592ee47305D9B3e10',
    'sender': '0x627306090abaB3A6e1400e9345bC60c78a8BEf57',
    'params': {
         'claimant': '0xf17f52151EbEF6C7334FAD080c5704D77216b732',
         'deadline': '1589280934319',
    }
}


releaseTimeIncreased = {
    'transactionHash': '0xe9aabe3feaf9fa8759ce2f86d673036c59b9a182398ee3c8913e4b4dea2b3e9b',
    'block': 35,
    'type': 'ReleaseTimeIncreased',
    'address': '0x345cA3e014Aaf5dcA488057592ee47305D9B3e10',
    'sender': '0xf17f52151EbEF6C7334FAD080c5704D77216b732',
    'params': {
         'stakeReleaseTime': '1589280934319'
    }
}


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
