from engine.testcases import EngineTestCase


class ModelsTest(EngineTestCase):
	def test_assets_saved_on_init(self):
		"""
		The game should save the corporation value on start
		"""

		self.assertEqual(self.c.assethistory_set.get(turn=0).assets, self.c.assets)
