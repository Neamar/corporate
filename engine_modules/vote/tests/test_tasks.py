import random

from engine.testcases import EngineTestCase
from engine_modules.vote.models import VoteOrder


class TaskTest(EngineTestCase):
	def setUp(self):
		super(TaskTest, self).setUp()

                self.c_corporation_market = random.choice(self.c.corporation_markets)
                self.c2_corporation_market = random.choice(self.c2.corporation_markets)

		self.v = VoteOrder(
			player=self.p,
			corporation_market_up=self.c_corporation_market,
			corporation_market_down=self.c2_corporation_market,
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
