import json
import time
import datetime
import ast

from app.rabbitmq_client import rabbitmq_client

from utilities.debug import pretty_print


def event_processor(ch, method, properties, body):

    # converts body from a byte string to a dictionary
    event = json.loads(body.decode())

    if event['type'] == 'StakeCreated':


    pretty_print(event)

    ch.basic_ack(delivery_tag = method.delivery_tag)


            rabbitmq_client.queue_declare(queue='delphi_events', durable=True)
            rabbitmq_client.basic_qos(prefetch_count=1)
            rabbitmq_client.basic_consume(event_processor, queue='delphi_events')
            rabbitmq_client.start_consuming()
