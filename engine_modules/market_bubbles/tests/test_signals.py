# -*- coding: utf-8 -*-
from django.dispatch import receiver

from engine.decorators import sender_instance_of
from engine.dispatchs import validate_order
from engine.exceptions import OrderNotAvailable

from django.core.exceptions import ValidationError

from engine.testcases import EngineTestCase
from engine_modules.market_bubbles.models import MarketBubble
from engine_modules.market.models import Market, CorporationMarket

class SignalsTest(EngineTestCase):
        def setUp(self):
                super(SignalsTest, self).setUp()

		self.b = MarketBubble(
			corporation = self.c,
			market = CorporationMarket.objects.filter(corporation=self.c)[0].market,
			turn = self.g.current_turn,
			value = 1,
		)
		self.b.save()


        def test_unique_domination_same_turn_same_corpo(self):

		b2 = MarketBubble(
			corporation = self.c,
			market = self.b.market,
			turn = self.g.current_turn,
			value = 1,
		)
		self.assertRaises(ValidationError, b2.save)

        def test_unique_domination_same_turn_different_corpo(self):
		# Can I assume I am guaranteed to have overlapping markets in c and c2 ??
		c_markets = [c.market for c in CorporationMarket.objects.filter(corporation=self.c)]
		c2_markets = [c.market for c in CorporationMarket.objects.filter(corporation=self.c2)]
		common_market = None
		for m in c_markets:
			if m in c2_markets:
				common_market = m

		if common_market == None:
			raise ValidationError("There is a problem with this test : no common market between c and c2")

		self.b.market = common_market
		self.b.save()

		b2 = MarketBubble(
			corporation = self.c2,
			market = common_market,
			turn = self.b.turn,
			value = 1,
		)
		self.assertRaises(ValidationError, b2.save)

        def test_unique_domination_different_turns(self):

		b2 = MarketBubble(
                        corporation = self.c,
                        market = self.b.market,
                        turn = self.g.current_turn + 1,
                        value = 1,
                )
		b2.save()

	def test_domination_market_in_corporation_markets(self):

		markets = Market.objects.all()
		corporation_markets = []
		for cm in CorporationMarket.objects.filter(corporation=self.c):
			corporation_markets.append(cm.market)

		absent_market = None
		for i in range(len(markets)):
			if markets[i] not in corporation_markets:
				absent_market = markets[i]

		self.b.market = absent_market 
		self.assertRaises(ValidationError, self.b.save)
