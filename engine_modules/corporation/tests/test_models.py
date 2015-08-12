from engine.testcases import EngineTestCase
from engine_modules.corporation.models import BaseCorporation, Corporation, AssetDelta


class ModelsTest(EngineTestCase):
	def test_corporation_auto_created(self):
		"""
		Corporation should have been created alongside the game
		"""

		corporations = Corporation.objects.all().order_by('base_corporation_slug')
		self.assertEqual(len(corporations), len(BaseCorporation.retrieve_all()))

		self.assertEqual(corporations[0].base_corporation.slug, 'c')


class ModelMethodTest(EngineTestCase):
	def test_corporation_update_assets(self):
		"""
		Corporation assets should be updated
		"""

		corporation_market = self.c.corporation_markets.last()
		initial_corporation_assets = self.c.assets
		initial_market_assets = corporation_market.value

		self.c.update_assets(-1, corporation_market=corporation_market, category=AssetDelta.EFFECT_FIRST)

		self.assertEqual(self.reload(self.c).assets, initial_corporation_assets - 1)
		self.assertEqual(self.reload(corporation_market).value, initial_market_assets - 1)
