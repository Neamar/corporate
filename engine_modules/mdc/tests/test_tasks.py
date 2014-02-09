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
			party_line=MDCVoteOrder.MDC_PARTY_LINE_CHOICES[2][0]
		)
		self.v.save()

	def test_party_line_set(self):
		"""
		Test the line is defined
		"""
		self.g.resolve_current_turn()
		
		mdc_vote_session = self.g.mdcvotesession_set.get(turn=self.g.current_turn)
		self.assertEqual(mdc_vote_session.current_party_line, self.v.party_line)

	def test_equality_no_party_line(self):
		"""
		When an equality occurs, no line is set
		"""
		self.v2 = MDCVoteOrder(
			player=self.p2,
			party_line=MDCVoteOrder.MDC_PARTY_LINE_CHOICES[3][0]
		)
		self.v2.save()

		self.g.resolve_current_turn()

		mdc_vote_session = (self.g.mdcvotesession_set.get(turn=self.g.current_turn))
		self.assertEqual(mdc_vote_session.current_party_line, None)

	def test_MDC_CPUB_line_effects(self):
		"""
		Test what happens when the CPUB party line is chosen
		"""

		initial_assets = self.c.assets
		initial_assets2 = self.c2.assets
		initial_assets3 = self.c3.assets
		
		self.v.party_line = MDCVoteOrder.MDC_PARTY_LINE_CHOICES[0][0]
		self.v.save()

		self.v2 = MDCVoteOrder(
			player=self.p2,
			party_line=MDCVoteOrder.MDC_PARTY_LINE_CHOICES[0][0]
		)
		self.v2.save()

		self.v3 = MDCVoteOrder(
			player=self.p3,
			party_line=MDCVoteOrder.MDC_PARTY_LINE_CHOICES[3][0]
		)
		self.v3.save()

		self.s = MDCVoteSession(
			current_party_line=MDCVoteOrder.MDC_PARTY_LINE_CHOICES[0][0],
			game=self.g,
			turn=self.g.current_turn
		)
		self.s.save()

		self.t = MDCLineCPUBTask()

		self.g.current_turn += 1
		self.g.save()
		self.t.run(self.g)

		self.assertEqual(self.reload(self.c).assets, initial_assets + 1)
		self.assertEqual(self.reload(self.c2).assets, initial_assets2 + 1)
		self.assertEqual(self.reload(self.c3).assets, initial_assets3 - 1)
