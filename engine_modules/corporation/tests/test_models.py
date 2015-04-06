import random

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

		corporation_market = self.c.corporationmarket_set.all().last()
		initial_corporation_assets = self.c.assets
		initial_market_assets = corporation_market.value

		self.c.update_assets(-1, market=corporation_market.market, category=AssetDelta.EFFECT_FIRST)

		self.assertEqual(self.reload(self.c).assets, initial_corporation_assets - 1)
		self.assertEqual(self.reload(corporation_market).value, initial_market_assets - 1)

	def test_corporation_update_assets_not_below_zero(self):
		"""
		Corporation market assets can't drop below 0
		"""

		c_markets = self.c.corporation_markets
		corporation_market = random.choice(c_markets)
		initial_corporation_assets = self.c.assets

		max_delta = corporation_market.value + 1
		self.c.update_assets(-max_delta, category=AssetDelta.EFFECT_FIRST, market=corporation_market.market)

		self.assertEqual(self.reload(self.c).assets, initial_corporation_assets - max_delta + 1)
		self.assertEqual(self.reload(corporation_market).value, 0)
