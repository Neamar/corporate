from engine.models import Player
from engine.testcases import EngineTestCase
from engine_modules.mdc.models import MDCVoteOrder
from engine_modules.share.models import Share
from engine_modules.corporation.models import Corporation


class TaskTest(EngineTestCase):
	def setUp(self):
		super(TaskTest, self).setUp()

		self.g.corporation_set.all().delete()
		self.c = Corporation(base_corporation_slug='renraku', assets=20)
		self.g.corporation_set.add(self.c)
		self.c2 = Corporation(base_corporation_slug='shiawase', assets=10)
		self.g.corporation_set.add(self.c2)

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
		p2 = Player(game=self.g)
		p2.save()

		self.v2 = MDCVoteOrder(
			player=p2,
			party_line=MDCVoteOrder.MDC_PARTY_LINE_CHOICES[3][0]
		)
		self.v2.save()

		self.g.resolve_current_turn()

		mdc_vote_session = (self.g.mdcvotesession_set.get(turn=self.g.current_turn))
		self.assertEqual(mdc_vote_session.current_party_line, None)
