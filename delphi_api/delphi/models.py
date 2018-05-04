# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.postgres.fields import JSONField

from django.db import models
from delphi.constants import STAGE_CHOICES, DRAFT_STAGE, EXPIRED_STAGE, ACTIVE_STAGE
from django.core.exceptions import ObjectDoesNotExist
from app.utils import calculate_token_value

class Token(models.Model):
    normalized_name = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    symbol = models.CharField(max_length=128)
    price_usd = models.FloatField(default=0, null=True)

class Stake(models.Model):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    staker = models.CharField(max_length=128)
    address = models.CharField(max_length=128) # address of contract
    minimum_fee = models.IntegerField()
    data = models.CharField(max_length=128)
    claim_deadline = models.DateTimeField()
    arbiter = models.CharField(max_length=128) # address of arbiter
    # whitelisted_claimants = ???
    # claims = ???
    # settlements = ???
    token = models.ForeignKey(Token, null=True)
    tokenSymbol = models.CharField(max_length=128, default='ETH')
    tokenDecimals = models.IntegerField(default=18)
    tokenLockPrice = models.FloatField(null=True, blank=True)
    tokenContract = models.CharField(
        max_length=128,
        default='0x0000000000000000000000000000000000000000')
    usd_price = models.FloatField(default=0)
