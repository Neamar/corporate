from engine.testcases import EngineTestCase
from engine_modules.corporation.models import Corporation, BaseCorporation

class TaskTest(EngineTestCase):
	"""
	Unit tests for invisible_hand task
	"""
	def test_invisible_hand_with_two_corpo(self):
		bc = BaseCorporation(name="bc1")
		bc.save()

		bc2 = BaseCorporation(name="bc2")
		bc2.save()

		c = Corporation(base_corporation=bc, game=self.g, assets=10)
		c.save()

		c2 = Corporation(base_corporation=bc2, game=self.g, assets=15)
		c2.save()

		self.g.resolve_current_turn()

		c = self.reload(c)
		c2 = self.reload(c2)

		self.assertNotEqual(c.assets, 10)
		self.assertNotEqual(c2.assets, 15)
		self.assertEqual(c.assets + c2.assets, 25)

	def test_invisible_hand_with_one_corpo(self):
		bc = BaseCorporation(name="bc1")
		bc.save()

		c = Corporation(base_corporation=bc, game=self.g, assets=10)
		c.save()

		self.g.resolve_current_turn()

		c = self.reload(c)

		self.assertEqual(c.assets, 11)