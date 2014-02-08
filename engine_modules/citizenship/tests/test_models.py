from engine.testcases import EngineTestCase
from engine_modules.corporation.models import Corporation


class ModelTest(EngineTestCase):
	def setUp(self):

		super(ModelTest, self).setUp()
		self.g.corporation_set.all().delete()
		self.c = Corporation(base_corporation_slug='shiawase', assets=10)
		self.g.corporation_set.add(self.c)
		self.c2 = Corporation(base_corporation_slug='renraku', assets=10)
		self.g.corporation_set.add(self.c2)

	def test_corporation_crashing_removes_citizenship(self):
		"""
		Corporation should have been created alongside the game
		"""

		self.p.citizenship.corporation = self.c
		self.p.citizenship.save()

		self.c.assets = 0
		self.c.save()

		self.g.resolve_current_turn()

		self.assertIsNone(self.reload(self.p).citizenship.corporation)
