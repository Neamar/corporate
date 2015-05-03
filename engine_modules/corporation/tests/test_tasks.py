from engine.testcases import EngineTestCase
from engine_modules.corporation.models import Corporation, AssetDelta


class CrashCorporationTaskTest(EngineTestCase):

	def test_corporation_deleted_when_market_assets_drop_to_zero(self):
		"""
		Corporations should crash when their market assets drop to 0
		"""

		self.c.market_assets = 0
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
				self.c.update_assets(-self.c.assets, AssetDelta.RUN_SABOTAGE, cm.market)
			cm.save()

		self.g.resolve_current_turn()

		self.assertRaises(Corporation.DoesNotExist, lambda: self.reload(self.c))

	def test_corporation_not_deleted_when_assets_not_zero(self):
		"""
		A corporation should not crash 
		"""
