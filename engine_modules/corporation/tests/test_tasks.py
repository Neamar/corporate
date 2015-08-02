from engine.testcases import EngineTestCase
from engine_modules.corporation.models import Corporation, AssetDelta


class CrashCorporationTaskTest(EngineTestCase):

	def test_corporation_deleted_when_market_assets_drop_to_zero(self):
		"""
		Corporations should crash when their market assets drop to 0
		"""

		self.c.set_market_assets(0)
		self.c.save()

		self.g.resolve_current_turn()

		self.assertRaises(Corporation.DoesNotExist, lambda: self.reload(self.c))

	def test_corporation_deleted_when_assets_drop_to_zero(self):
		"""
		Corporations should actually crash as soon as their assets drop to 0
		This is a different test from test_corporation_deleted_when_market_assets_drop_to_zero, because we have to take the MarketBubbles into account
		"""

		corporation_markets = self.c.corporation_markets

		for cm in corporation_markets:
			if self.c.assets > 0:
				# because a market cannot be negative, this ensures that at the end, Corporation's assets will be exactly 0
				# unfortunately, because bubbles are only computed in resolve_current_turn, this also ensures that each market has value 0 ...
				corporation_market = self.c.corporationmarket_set.get(market=cm.market, turn=self.g.current_turn)
				self.c.update_assets(delta=-self.c.assets, category=AssetDelta.RUN_SABOTAGE, corporation_market=corporation_market)
			cm.save()

		self.g.resolve_current_turn()

		self.assertRaises(Corporation.DoesNotExist, lambda: self.reload(self.c))

	def test_corporation_not_deleted_when_assets_not_zero(self):
		"""
		A corporation should not crash when it has one market asset at 0 but not its assets
		"""

		corporation_market = self.c.get_random_corporation_market()
		corporation_market.value = 100
		corporation_market.save()

		negative_corporation_market = self.c.get_random_corporation_market()
		while negative_corporation_market == corporation_market:
			negative_corporation_market = self.c.get_random_corporation_market()

		negative_corporation_market.value = -10
		negative_corporation_market.save()

		self.reload(self.c)
