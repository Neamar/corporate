from engine.testcases import EngineTestCase
from engine_modules.vote.models import VoteOrder

class TaskTest(EngineTestCase):
	def setUp(self):
		
		super(TaskTest, self).setUp()

		self.c = self.g.corporation_set.get(base_corporation_slug="renraku")
		self.c2 = self.g.corporation_set.get(base_corporation_slug="shiawase")

		self.v = VoteOrder(
			player=self.p,
			corporation_up=self.c,
			corporation_down=self.c2
		)
		self.v.save()

		# Disable invisible_hand for reliable results
		self.g.disable_invisible_hand = True

	def test_vote(self):
		begin_assets_1 = self.c.assets
		begin_assets_2 = self.c2.assets

		self.g.resolve_current_turn()

		self.c = self.reload(self.c)
		self.c2 = self.reload(self.c2)

		self.assertEqual(self.c.assets, begin_assets_1 + 1)
		self.assertEqual(self.c2.assets, begin_assets_2 - 1)
