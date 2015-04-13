from engine.testcases import EngineTestCase


class TaskTest(EngineTestCase):
	def setUp(self):

		super(TaskTest, self).setUp()
		self.g.force_bubbles = True

# TODO: Modify the test to be more specific
	def test_increase_assets(self):

		begin_assets_1 = self.c.assets
		begin_assets_2 = self.c2.assets

		self.g.resolve_current_turn()

		self.c = self.reload(self.c)
		self.c2 = self.reload(self.c2)

		self.assertNotEqual(self.c.assets, begin_assets_1)
		self.assertNotEqual(self.c2.assets, begin_assets_2)
