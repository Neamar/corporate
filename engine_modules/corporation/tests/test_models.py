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

		initial_assets = corporation.assets
		corporation.update_assets(-1)
		self.assertEqual(self.reload(corporation).assets, initial_assets - 1)
