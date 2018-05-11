import json
import time
from datetime import datetime, timedelta
import ast
from decimal import Decimal

import sys
sys.path.append('/usr/src/app')

from app.migrations.models import Stake, Whitelistee
from app.util.connection import connect
from sqlalchemy.orm import sessionmaker
from app.util.logging import pretty_print
from app.event_processor.rabbitmq import client

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

def message_handler(ch, method, properties, body):

    # converts body from a byte string to a dictionary
    event = json.loads(body.decode())

    event_processor(event)

    # pretty_print(event)

    ch.basic_ack(delivery_tag = method.delivery_tag)

def event_processor(event):
    if event.get('type') == 'StakeCreated':

        params = event.get('params')

        stake = Stake(
            event.get('address'),
            event.get('sender'),
            int(Decimal( params.get('value') )),
            params.get('data'),
            int(Decimal( params.get('minimumFee') )),
            int(Decimal( params.get('stakeReleaseTime') ))
        )

        session.add(stake)
        session.commit()

    if event.get('type') == 'ClaimantWhitelisted':
        params = event.get('params')

        whitelistee = Whitelistee(
            event.get('address'),
            params.get('claimant'),
            int(Decimal( params.get('deadline') ))
        )

        stake = session.query(Stake).filter_by(address=event.get('address')).first()
        stake.whitelist.append(whitelistee)

        session.add_all([stake, whitelistee])
        session.commit()

if __name__ == "__main__":
    client.basic_consume(message_handler, queue='delphi_events')
    client.start_consuming()
