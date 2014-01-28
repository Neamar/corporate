from engine.testcases import EngineTestCase
from engine_modules.corporation.models import BaseCorporation

class TaskTest(EngineTestCase):
	def setUp(self):
		self.bc = BaseCorporation("renraku")
		self.bc2 = BaseCorporation("shiawase")
		
		super(TaskTest, self).setUp()

		self.c = self.g.corporation_set.get(base_corporation_slug=self.bc.slug)
		self.c.assets=10
		self.c.save()
		self.c2 = self.g.corporation_set.get(base_corporation_slug=self.bc2.slug)
		self.c2.assets=10
		self.c2.save()

	def test_invisible_hand_with_two_corporations(self):
		self.c2.assets = 15
		self.c2.save()

		begin_assets_1 = self.c.assets
		begin_assets_2 = self.c2.assets
		begin_assets_sum = self.c.assets + self.c2.assets
		self.g.resolve_current_turn()

		self.c = self.reload(self.c)
		self.c2 = self.reload(self.c2)

		self.assertNotEqual(self.c.assets, begin_assets_1)
		self.assertNotEqual(self.c2.assets, begin_assets_2)
		self.assertEqual(self.c.assets + self.c2.assets, begin_assets_sum)

	def test_invisible_hand_with_one_corporation(self):
		begin_assets = self.c.assets

		self.c2.delete()
		self.g.resolve_current_turn()

		self.assertEqual(self.reload(self.c).assets, begin_assets + 1)
