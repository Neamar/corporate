from engine.testcases import EngineTestCase
from engine_modules.corporation.models import Corporation


class ModelsTest(EngineTestCase):
	"""
	Unit tests for engine models
	"""
	def setUp(self):

		super(ModelsTest, self).setUp()
		self.g.corporation_set.all().delete()
		self.c = Corporation(base_corporation_slug='shiawase', assets=10)
		self.g.corporation_set.add(self.c)

	def test_assets_saved_on_init(self):
		"""
		The game should save the corporation value on start
		"""

		self.assertEqual(self.c.assethistory_set.get(turn=0).assets, self.c.assets)
