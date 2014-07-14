from engine.testcases import EngineTestCase
from engine_modules.vote.models import VoteOrder


class TaskTest(EngineTestCase):
	def setUp(self):
		super(TaskTest, self).setUp()

		self.c_market = self.c.corporationmarket_set.get(market=self.c.historic_market).market
		self.c2_market = self.c.corporationmarket_set.get(market=self.c2.historic_market).market

		self.v = VoteOrder(
			player=self.p,
			corporation_up=self.c,
			market_up=self.c_market,
			corporation_down=self.c2,
			market_down=self.c2_market,
		)
		self.v.save()

	def test_vote(self):
		begin_assets_1 = self.c.assets
		begin_assets_2 = self.c2.assets

		self.g.resolve_current_turn()

		self.c = self.reload(self.c)
		self.c2 = self.reload(self.c2)

		self.assertEqual(self.c.assets, begin_assets_1 + 1)
		self.assertEqual(self.c2.assets, begin_assets_2 - 1)
