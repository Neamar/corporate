from engine.testcases import EngineTestCase


class TaskTest(EngineTestCase):
	def setUp(self):

		super(TaskTest, self).setUp()
		self.g.force_invisible_hand = True
		self.c3.delete()

	def test_invisible_hand_with_two_corporations(self):

		self.c2.set_market_assets(15)

		begin_assets_1 = self.c.assets
		begin_assets_2 = self.c2.assets
		begin_assets_sum = self.c.assets + self.c2.assets
		self.g.resolve_current_turn()

		self.c = self.reload(self.c)
		self.c2 = self.reload(self.c2)

		self.assertNotEqual(self.c.assets, begin_assets_1)
		self.assertNotEqual(self.c2.assets, begin_assets_2)
		self.assertEqual(self.c.assets + self.c2.assets, begin_assets_sum)
