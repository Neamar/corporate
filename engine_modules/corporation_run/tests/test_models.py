from engine.testcases import EngineTestCase
from engine_modules.corporation_run.models import DataStealOrder, ProtectionOrder


class ModelsTest(EngineTestCase):
	def setUp(self):
		super(ModelsTest, self).setUp()

		# We disable the test that stop you from start more than one run on the same target
		self.g.allow_several_runs_on_one_target = True
		
		common_corporation_market = self.c.get_common_corporation_market(self.c2)

		self.dso = DataStealOrder(
			player=self.p,
			target_corporation_market=common_corporation_market,
			stealer_corporation=self.c2,
		)
		self.dso.save()

	def test_target_corporation_property(self):
		"""
		target_corporation must return the right corporation
		"""
		self.assertEqual(self.dso.target_corporation, self.c)

	def test_stealer_corporation_market_property(self):
		"""
		stealer_corporation_market must return the right corporation_market
		"""
		self.assertEqual(self.dso.stealer_corporation_market, self.c2.corporationmarket_set.get(market=self.dso.target_corporation_market.market, turn=self.g.current_turn))

	def test_protected_corporation_property(self):
		"""
		protected_corporation must return the right corporation
		"""

		po = ProtectionOrder(
			player=self.p,
			protected_corporation_market=self.c.get_random_corporation_market(),
		)
		po.save()

		self.assertEqual(po.protected_corporation, self.c)
