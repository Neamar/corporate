from engine.testcases import EngineTestCase


class ModelsTest(EngineTestCase):
	def test_corporation_crashing_removes_citizenship(self):
		"""
		Corporation crash should set citizenship to null
		"""

		self.p.citizenship.corporation = self.c
		self.p.citizenship.save()

		self.c.assets = 0
		self.c.save()

		self.g.resolve_current_turn()

		self.assertIsNone(self.reload(self.p).citizenship.corporation)
