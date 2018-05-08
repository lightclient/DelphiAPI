import json
import time
from datetime import datetime
import ast


import sys
sys.path.append('/usr/src/app')

from app.migrations.models import Stake, Whitelistee
from app.util.connection import connect
from sqlalchemy.orm import sessionmaker
from app.util.logging import pretty_print
from rabbitmq import client

engine = connect()

Session = sessionmaker(bind=engine)
session = Session()

# w = Whitelistee(
#     s.address,
#     '0x0000000000000000000000000000000000000001',
#     datetime.now() + timedelta(days=21)
# )
#
# s.whitelist.append(w)

def event_processor(ch, method, properties, body):

    # converts body from a byte string to a dictionary
    event = json.loads(body.decode())

    if event['type'] == 'StakeCreated':
        stake = Stake(
            event.get('stake'),
            event.get('staker'),
            float( event.get('claimable_stake') ),
            event.get('data'),
            float( event.get('minimum_fee') ),
            datetime.fromtimestamp( int(event.get('release_time')) )
        )

        session.add(stake)
        session.commit()

    if event.get('type') == 'ClaimantWhitelisted':
        whitelistee = Whitelistee(
            event.get('claimaint')
        )

    pretty_print(event)

    ch.basic_ack(delivery_tag = method.delivery_tag)

client.basic_consume(event_processor, queue='delphi_events')
client.start_consuming()
