from django.test import TestCase
from engine.models import Game
from engine.testcases import EngineTestCase
from engine_modules.corporation.models import BaseCorporation, Corporation


class ModelsTest(TestCase):
	"""
	Inherit from TestCase and not from EngineTestCase, since EngineTestCase overrides base corporation behavior for faster tests.
	"""

	def setUp(self):

		self.g = Game()
		self.g.save()

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

		corporation = Corporation.objects.get(base_corporation_slug='c')

		corporation_market = corporation.corporationmarket_set.all().last()
		initial_corporation_assets = corporation.assets
		initial_market_assets = corporation_market.value

		corporation.update_assets(-1, market=corporation_market.market)

		self.assertEqual(self.reload(corporation).assets, initial_corporation_assets - 1)
		self.assertEqual(self.reload(corporation_market).value, initial_market_assets - 1)

	def test_corporation_update_assets_in_historic_market(self):
		"""
		Corporation assets should be updated in historic market by default
		"""

		corporation = Corporation.objects.get(base_corporation_slug='c')

		corporation_historic_market = corporation.corporationmarket_set.get(market=corporation.historic_market)
		initial_corporation_assets = corporation.assets
		initial_market_assets = corporation_historic_market.value

		corporation.update_assets(-1)

		self.assertEqual(self.reload(corporation).assets, initial_corporation_assets - 1)
		self.assertEqual(self.reload(corporation_historic_market).value, initial_market_assets - 1)

	def test_corporation_update_assets_not_below_zero(self):
		"""
		Corporation assets should be updated in historic market by default
		"""

		corporation = Corporation.objects.get(base_corporation_slug='c')

		corporation_historic_market = corporation.corporationmarket_set.get(market=corporation.historic_market)
		initial_corporation_assets = corporation.assets

		max_delta = corporation_historic_market.value + 1
		corporation.update_assets(-max_delta)

		self.assertEqual(self.reload(corporation).assets, initial_corporation_assets - max_delta + 1)
		self.assertEqual(self.reload(corporation_historic_market).value, 0)
