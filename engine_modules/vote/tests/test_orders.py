from django.core.exceptions import ValidationError

from engine.testcases import EngineTestCase
from engine.exceptions import OrderNotAvailable
from engine_modules.vote.models import VoteOrder
from engine_modules.market.models import Market


class OrdersTest(EngineTestCase):
	def setUp(self):
		super(OrdersTest, self).setUp()
		self.c_market = self.c.corporationmarket_set.get(market=self.c.historic_market).market
		self.c2_market = self.c.corporationmarket_set.get(market=self.c2.historic_market).market

	def test_corporation_up_and_down(self):

		begin_assets_1 = self.c.assets
		begin_assets_2 = self.c2.assets
		o = VoteOrder(
			corporation_up=self.c,
			market_up=self.c_market,
			corporation_down=self.c2,
			market_down=self.c2_market,
			player=self.p
		)
		o.save()

		o.resolve()

		self.assertEqual(self.reload(self.c).assets, begin_assets_1 + 1)
		self.assertEqual(self.reload(self.c2).assets, begin_assets_2 - 1)

	def test_cant_vote_more_than_once(self):
		o = VoteOrder(
			corporation_up=self.c,
			market_up=self.c_market,
			corporation_down=self.c2,
			market_down=self.c2_market,
			player=self.p
		)
		# assertNoRaises
		o.save()

		o2 = VoteOrder(
			corporation_up=self.c,
			corporation_down=self.c2,
			player=self.p
		)

		self.assertRaises(OrderNotAvailable, o2.clean)

	def test_cant_vote_nonexisting_market_up(self):
		m = Market(
			name="non_existing",
			game=self.g
		)
		m.save()

		o = VoteOrder(
			corporation_up=self.c,
			market_up=m,
			corporation_down=self.c2,
			market_down=self.c2_market,
			player=self.p
		)
		self.assertRaises(ValidationError, o.clean)

	def test_cant_vote_nonexisting_market_down(self):
		m = Market(
			name="non_existing",
			game=self.g
		)
		m.save()

		o = VoteOrder(
			corporation_up=self.c,
			market_up=self.c_market,
			corporation_down=self.c2,
			market_down=m,
			player=self.p
		)
		self.assertRaises(ValidationError, o.clean)
