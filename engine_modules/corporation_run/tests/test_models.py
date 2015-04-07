import random

from engine.testcases import EngineTestCase
from engine_modules.corporation_run.models import DataStealOrder, ProtectionOrder


class ModelsTest(EngineTestCase):
	def setUp(self):
		super(ModelsTest, self).setUp()

		common_market = self.c.get_common_market(self.c2)
		if common_market == None:
			raise ValidationError("There is a problem with this test : no common market between c and c2")

		self.dso = DataStealOrder(
			player=self.p,
			target_corporation_market=common_market,
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
		self.assertEqual(self.dso.stealer_corporation_market, self.c2.corporationmarket_set.get(market=self.dso.target_corporation_market.market))

	def test_protected_corporation_property(self):
		"""
		protected_corporation must return the right corporation
		"""

		po = ProtectionOrder(
			player=self.p,
			protected_corporation_market=random.choice(self.c.corporation_markets),
		)
		po.save()

		self.assertEqual(po.protected_corporation, self.c)
