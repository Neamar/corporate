from engine.testcases import EngineTestCase
from engine_modules.corporation.models import BaseCorporation

class TaskTest(EngineTestCase):
	"""
	Unit tests for invisible_hand task
	"""
	def setUp(self):
		self.bc = BaseCorporation(name="bc1")
		self.bc.save()

		self.bc2 = BaseCorporation(name="bc2")
		self.bc2.save()
		
		super(TaskTest, self).setUp()

		self.c = self.g.corporation_set.get(base_corporation=self.bc)
		self.c2 = self.g.corporation_set.get(base_corporation=self.bc2)

	def test_invisible_hand_with_two_corporations(self):
		self.c2.assets = 15
		self.c2.save()
		self.g.resolve_current_turn()

		self.c = self.reload(self.c)
		self.c2 = self.reload(self.c2)

		self.assertNotEqual(self.c.assets, 10)
		self.assertNotEqual(self.c2.assets, 15)
		self.assertEqual(self.c.assets + self.c2.assets, 25)

	def test_invisible_hand_with_one_corporation(self):
		self.g.resolve_current_turn()

		self.assertEqual(self.reload(self.c).assets, 11)
