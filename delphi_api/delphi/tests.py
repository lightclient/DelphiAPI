# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from functools import partial

from django.test import TestCase

# Create your tests here.
from utils.functional_tools import narrower, formatter, merge, pipe

import logging

class BountySubscriberTest(TestCase):
    def nop():
        print('nop')
