from engine.testcases import EngineTestCase
from engine_modules.corporation.models import BaseCorporation


class ModelsTest(EngineTestCase):
	"""
	Unit tests for engine models
	"""
	def setUp(self):
		self.bc = BaseCorporation("renraku")

		super(ModelsTest, self).setUp()

		self.c = self.g.corporation_set.get(base_corporation_slug=self.bc.slug)

	def test_assets_saved_on_init(self):
		"""
		The game should save the corporation value on start
		"""

		self.assertEqual(self.c.assethistory_set.get(turn=0).assets, self.c.assets)
