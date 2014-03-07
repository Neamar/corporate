from engine.models import Player
from engine.testcases import EngineTestCase
from engine_modules.mdc.models import MDCVoteOrder


class TaskTest(EngineTestCase):
	def setUp(self):
		super(TaskTest, self).setUp()

		self.p2 = Player(game=self.g)
		self.p2.save()

		self.v = MDCVoteOrder(
			player=self.p,
			coalition=MDCVoteOrder.DERE
		)
		self.v.save()

	def test_coalition_set(self):
		"""
		Test the line is defined
		"""
		self.g.resolve_current_turn()

		mdc_vote_session = self.g.mdcvotesession_set.get(turn=self.g.current_turn)
		self.assertEqual(mdc_vote_session.coalition, self.v.coalition)

	def test_equality_no_coalition(self):
		"""
		When an equality occurs, no line is set
		"""
		self.v2 = MDCVoteOrder(
			player=self.p2,
			coalition=MDCVoteOrder.DEVE
		)
		self.v2.save()

		self.g.resolve_current_turn()

		mdc_vote_session = (self.g.mdcvotesession_set.get(turn=self.g.current_turn))
		self.assertEqual(mdc_vote_session.coalition, None)
