import json
import time
import datetime
import ast

from django.core.management.base import BaseCommand

#from std_bounties import master_client
#from bounties.sqs_client import sqs_client
from django.conf import settings
#from bounties.redis_client import redis_client
from app.rabbitmq_client import rabbitmq_client
#from std_bounties.models import Event
#import logging
from utils.debug import pretty_print

#logger = logging.getLogger('django')

def event_processor(ch, method, properties, body):

    event = json.loads(body.decode())
    pretty_print( [ ('Event Name',event['eventName']) ] )

    ch.basic_ack(delivery_tag = method.delivery_tag)

    # '{"eventName":"StakeCreated",
    # "stakeAddress":"0x345cA3e014Aaf5dcA488057592ee47305D9B3e10",
    # "staker":"0x627306090abaB3A6e1400e9345bC60c78a8BEf57",
    # "claimableStake":"100",
    # "token":"0x8f0483125FCb9aaAEFA9209D8E9d7b9C8B9Fb90F",
    # "minimumFee":"10",
    # "data":"i love cats",
    # "stakeReleaseTime":"1525421121",
    # "arbiter":"0xbaAA2a3237035A2c7fA2A33c76B44a8C6Fe18e87"}'

    # if event == 'PayoutIncreased':
    #     master_client.payout_increased(bounty_id, inputs=contract_method_inputs)

    #logger.info(event)

    # This means the contract subscriber will never send this event
    # through to sqs again

    # Event.objects.get_or_create(
    #     event=event,
    #     transaction_hash=transaction_hash,
    #     defaults = {
    #         'bounty_id': bounty_id,
    #         'fulfillment_id': fulfillment_id if fulfillment_id != -1 else None,
    #         'transaction_from': transaction_from,
    #         'contract_inputs': contract_method_inputs,
    #         'event_date': datetime.datetime.fromtimestamp(int(event_timestamp))
    #     }
    # )

    # redis_client.set(message_deduplication_id, True)

class Command(BaseCommand):
    help = 'Listen to SQS queue for contract events'

    def handle(self, *args, **options):
        try:

            rabbitmq_client.queue_declare(queue='delphi_events', durable=True)
            rabbitmq_client.basic_qos(prefetch_count=1)
            rabbitmq_client.basic_consume(event_processor, queue='delphi_events')
            rabbitmq_client.start_consuming()

        except Exception as e:
            # goes to rollbar
            # logger.exception(e)
            raise e
