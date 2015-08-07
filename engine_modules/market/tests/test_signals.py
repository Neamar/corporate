# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError

from engine.testcases import EngineTestCase


class SignalsTest(EngineTestCase):

	def setUp(self):

		super(SignalsTest, self).setUp()

	def test_unique_domination_same_market_same_turn(self):
		"""
		A Market should only have one domination bubble per turn
		A bubble should give a bonus or a malus of 1, so a CorporationMarket should have
		a bubble_value of either -1, 0, or 1
		"""

		cm = self.c.get_random_corporation_market()
		cm.bubble_value = 2
		self.assertRaises(ValidationError, cm.save)
