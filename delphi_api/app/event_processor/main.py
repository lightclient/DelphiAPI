import json
import time
import datetime
import ast

import sys
# Add the ptdraft folder path to the sys.path list
sys.path.append('/usr/src/app')

from app.util.logging import pretty_print
from rabbitmq import client

def event_processor(ch, method, properties, body):

    # converts body from a byte string to a dictionary
    event = json.loads(body.decode())

    if event['type'] == 'StakeCreated':
        print("new stake")

    pretty_print(event)

    ch.basic_ack(delivery_tag = method.delivery_tag)

client.basic_consume(event_processor, queue='delphi_events')
client.start_consuming()
