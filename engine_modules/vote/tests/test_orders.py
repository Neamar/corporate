from engine.testcases import EngineTestCase
from engine.exceptions import OrderNotAvailable
from engine_modules.vote.models import VoteOrder


class OrdersTest(EngineTestCase):
	def setUp(self):
		super(OrdersTest, self).setUp()
		self.c_corporation_market = self.c.random_corporation_market
		self.c2_corporation_market = self.c2.random_corporation_market

	def test_corporation_up_and_down(self):

		begin_assets_1 = self.c.assets
		begin_assets_2 = self.c2.assets
		o = VoteOrder(
			corporation_market_up=self.c_corporation_market,
			corporation_market_down=self.c2_corporation_market,
			player=self.p
		)
		o.save()

		o.resolve()

		self.assertEqual(self.reload(self.c).assets, begin_assets_1 + 1)
		self.assertEqual(self.reload(self.c2).assets, begin_assets_2 - 1)

	def test_cant_vote_more_than_once(self):
		o = VoteOrder(
			corporation_market_up=self.c_corporation_market,
			corporation_market_down=self.c2_corporation_market,
			player=self.p
		)
		# assertNoRaises
		o.save()

		o2 = VoteOrder(
			corporation_market_up=self.c_corporation_market,
			corporation_market_down=self.c2_corporation_market,
			player=self.p
		)

		self.assertRaises(OrderNotAvailable, o2.clean)
