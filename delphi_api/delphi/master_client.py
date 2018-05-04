from functools import partial, update_wrapper
from decimal import Decimal

from app import settings
from delphi.bounty_client import BountyClient
from delphi.client_helpers import bounty_url_for, apply_and_notify, formatted_fulfillment_amount, token_price, format_deadline, usd_price, token_lock_price
from utils.functional_tools import merge, narrower, wrapped_partial

from slackclient import SlackClient


bounty_client = BountyClient()
sc = SlackClient(settings.SLACK_TOKEN)


# @with_clients
# def bounty_issued(bounty_id, **kwargs):
#     msg = "{title}, id: {bounty_id}\n${usd_price}, {total_value} {tokenSymbol} @ ${token_price}\n" \
#           "Deadline: {deadline}\n{link} :tada:"
#     bounty = Bounty.objects.filter(bounty_id=bounty_id)
#     add_link = partial(merge, source2={'link': bounty_url_for(bounty_id)})
#
#     if not bounty.exists():
#         apply_and_notify(bounty_id,
#                          event='Bounty Issued',
#                          action=bounty_client.issue_bounty,
#                          inputs=kwargs,
#                          fields=['title', 'bounty_id', 'tokenSymbol', 'tokenDecimals',
#                                  'fulfillmentAmount', 'usd_price', 'deadline', 'token'],
#                          msg=msg,
#                          slack_client=sc,
#                          before_formatter=[add_link, formatted_fulfillment_amount, token_price, format_deadline, usd_price]
#                          )
