from engine.testcases import EngineTestCase


class TaskTest(EngineTestCase):
	def setUp(self):

		super(TaskTest, self).setUp()
		self.g.force_invisible_hand = True
		self.c3.delete()

	def test_invisible_hand_with_two_corporations(self):
		self.c2.market_assets = 15
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
