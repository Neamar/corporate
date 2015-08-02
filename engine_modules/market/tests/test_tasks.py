# -*- coding: utf-8 -*-
from engine.testcases import EngineTestCase


class ReplicateCorporationMarketTaskTest(EngineTestCase):
	def setUp(self):

		super(ReplicateCorporationMarketTaskTest, self).setUp()

	def test_replicate_corporationmarket_task(self):
		"""
		Test that the CorporationMakets are correct for different turns
		"""

		market = self.c.markets[0]
		corporation_market = self.c.corporationmarket_set.get(market=market, turn=0)
		t0_val = corporation_market.value
		corporation_market = self.c.corporationmarket_set.get(market=market, turn=self.g.current_turn)
		corporation_market.value = t0_val + 1
		corporation_market.save()
		self.g.resolve_current_turn()

		corporation_market = self.reload(self.c).corporationmarket_set.get(market=market, turn=1)
		t1_val = corporation_market.value
		corporation_market = self.c.corporationmarket_set.get(market=market, turn=self.g.current_turn)
		corporation_market.value = t1_val + 3
		corporation_market.save()
		self.g.resolve_current_turn()

		corporation_market = self.reload(self.c).corporationmarket_set.get(market=market, turn=2)
		t2_val = corporation_market.value

		self.assertEqual(t1_val, t0_val + 1)
		self.assertEqual(t2_val, t1_val + 3)
