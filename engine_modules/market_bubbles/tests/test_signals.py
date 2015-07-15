# -*- coding: utf-8 -*-
import random

from django.core.exceptions import ValidationError

from engine.testcases import EngineTestCase
from engine_modules.market_bubbles.models import MarketBubble
from engine_modules.market.models import Market


class SignalsTest(EngineTestCase):

	def setUp(self):

		super(SignalsTest, self).setUp()
		self.b = MarketBubble(
			corporation=self.c,
			market=self.c.get_random_market(),
			turn=self.g.current_turn,
			value=1,
		)
		self.b.save()

	def test_unique_domination_same_market_same_turn(self):
		"""
		A Market should only have one domination bubble per turn
		"""

		common_market = self.c.get_common_market(self.c2)
		self.b.market = common_market
		self.b.save()

		b2 = MarketBubble(
			corporation=self.c2,
			market=common_market,
			turn=self.b.turn,
			value=1,
		)
		self.assertRaises(ValidationError, b2.save)

	def test_unique_domination_different_turns(self):

		b2 = MarketBubble(
			corporation=self.c,
			market=self.b.market,
			turn=self.g.current_turn + 1,
			value=1,
		)
		b2.save()

	def test_domination_market_in_corporations_markets(self):

		markets = Market.objects.all()
		c_markets = self.c.markets
		absent_markets = [m for m in markets if m not in c_markets]

		self.b.market = random.choice(absent_markets)
		self.assertRaises(ValidationError, self.b.save)
