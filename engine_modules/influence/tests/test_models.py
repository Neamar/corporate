from engine.testcases import EngineTestCase


class ModelsTest(EngineTestCase):
	def test_influence_auto_created(self):
		"""
		The new player should have influence of 1
		"""
		self.assertEqual(self.p.influence.level, 1)
