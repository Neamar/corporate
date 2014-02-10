from engine.models import Player
from engine.testcases import EngineTestCase
from engine_modules.share.models import Share
from engine_modules.mdc.models import MDCVoteOrder, MDCVoteSession
from engine_modules.corporation.models import Corporation

from engine_modules.mdc.tasks import MDCLineCPUBTask

class TaskTest(EngineTestCase):
	def setUp(self):
		super(TaskTest, self).setUp()

		self.p2 = Player(game=self.g)
		self.p2.save()

		self.p3 = Player(game=self.g)
		self.p3.save()

		self.g.corporation_set.all().delete()
		self.c = Corporation(base_corporation_slug='renraku', assets=20)
		self.g.corporation_set.add(self.c)
		self.c2 = Corporation(base_corporation_slug='shiawase', assets=10)
		self.g.corporation_set.add(self.c2)
		self.c3 = Corporation(base_corporation_slug='ares', assets=10)
		self.g.corporation_set.add(self.c3)

		self.s = Share(
			corporation=self.c,
			player=self.p,
			turn=self.g.current_turn
		)
		self.s.save()

		self.s2 = Share(
			corporation=self.c2,
			player=self.p2,
			turn=self.g.current_turn
		)
		self.s2.save()

		self.s3 = Share(
			corporation=self.c3,
			player=self.p3,
			turn=self.g.current_turn
		)
		self.s3.save()

		self.v = MDCVoteOrder(
			player=self.p,
			party_line=MDCVoteOrder.DERE
		)
		self.v.save()

		self.v2 = MDCVoteOrder(
			player=self.p2,
			party_line=MDCVoteOrder.CPUB
		)
		self.v2.save()

		self.v3 = MDCVoteOrder(
			player=self.p3,
			party_line=MDCVoteOrder.DEVE
		)
		self.v3.save()

		self.g.disable_invisible_hand = True
		self.g.save()


	def test_MDC_CPUB_line_effects(self):
		"""
		Test what happens when the CPUB party line is chosen
		"""

		initial_assets = self.c.assets
		initial_assets2 = self.c2.assets
		initial_assets3 = self.c3.assets
		
		self.v.party_line = MDCVoteOrder.CPUB
		self.v.save()

		self.v2.party_line = MDCVoteOrder.CPUB
		self.v2.save()

		self.v3.party_line = MDCVoteOrder.DEVE
		self.v3.save()

		self.g.resolve_current_turn()

		# We have to resolve twice: once for the MDCVoteOrders to be taken into account
		# And once for the resulting MDCVoteSession to be effective
		self.g.resolve_current_turn()

		self.assertEqual(self.reload(self.c).assets, initial_assets + 1)
		self.assertEqual(self.reload(self.c2).assets, initial_assets2 + 1)
		self.assertEqual(self.reload(self.c3).assets, initial_assets3 - 1)
