import datetime
from decimal import Decimal
from delphi.constants import DRAFT_STAGE, ACTIVE_STAGE, DEAD_STAGE, COMPLETED_STAGE, EXPIRED_STAGE
from delphi.client_helpers import map_bounty_data, map_token_data, map_fulfillment_data, get_token_pricing, get_historic_pricing
from app.utils import getDateTimeFromTimestamp
from django.db import transaction
import logging


logger = logging.getLogger('django')

issue_bounty_input_keys = [
    'fulfillmentAmount',
    'arbiter',
    'paysTokens',
    'tokenContract',
    'value']


class BountyClient:

    def __init__(self):
        pass

    # @transaction.atomic
    # def issue_bounty(self, bounty_id, inputs, event_timestamp):
    #     data_hash = inputs.get('data', 'invalid')
    #     event_date = datetime.datetime.fromtimestamp(int(event_timestamp))
    #     ipfs_data = map_bounty_data(data_hash, bounty_id)
    #     token_data = map_token_data(
    #         inputs.get('paysTokens'),
    #         inputs.get('tokenContract'),
    #         inputs.get('fulfillmentAmount'))
    #
    #     plucked_inputs = {key: inputs.get(key)
    #                       for key in issue_bounty_input_keys}
    #
    #     bounty_data = {
    #         'id': bounty_id,
    #         'bounty_id': bounty_id,
    #         'issuer': inputs.get(
    #             'issuer',
    #             '').lower(),
    #         'deadline': getDateTimeFromTimestamp(
    #             inputs.get(
    #                 'deadline',
    #                 None)),
    #         'bountyStage': DRAFT_STAGE,
    #         'bounty_created': event_date,
    #     }
    #
    #     bounty_serializer = BountySerializer(
    #         data={
    #             **bounty_data,
    #             **plucked_inputs,
    #             **ipfs_data,
    #             **token_data})
    #     bounty_serializer.is_valid(raise_exception=True)
    #     saved_bounty = bounty_serializer.save()
    #     saved_bounty.save_and_clear_categories(
    #         ipfs_data.get('data_categories'))
    #     saved_bounty.record_bounty_state(event_date)
    #     return saved_bounty
