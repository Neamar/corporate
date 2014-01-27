from engine.testcases import EngineTestCase
from engine_modules.corporation.models import BaseCorporation
from engine_modules.vote.models import VoteOrder

class TaskTest(EngineTestCase):
	def setUp(self):
		self.bc = BaseCorporation("renraku")
		self.bc.save()

		self.bc2 = BaseCorporation("shiawase")
		self.bc2.save()
		
		super(TaskTest, self).setUp()

		self.c = self.g.corporation_set.get(base_corporation=self.bc)
		self.c2 = self.g.corporation_set.get(base_corporation=self.bc2)

		self.v = VoteOrder(
			player=self.p,
			corporation_up=self.c,
			corporation_down=self.c2
		)
		self.v.save()

		# Disable invisible_hand for reliable results
		self.g.disable_invisible_hand = True

	def test_vote(self):
		self.g.resolve_current_turn()

		self.c = self.reload(self.c)
		self.c2 = self.reload(self.c2)

		self.assertEqual(self.c.assets, 11)
		self.assertEqual(self.c2.assets, 9)
