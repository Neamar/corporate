# -*- coding: utf-8 -*-
from engine.models import Player
from engine.testcases import EngineTestCase
from engine_modules.share.models import Share
from engine_modules.detroit_inc.models import DIncVoteOrder


class TaskTest(EngineTestCase):
	def setUp(self):
		super(TaskTest, self).setUp()

		self.p2 = Player(game=self.g)
		self.p2.save()

		self.v = DIncVoteOrder(
			player=self.p,
			coalition=DIncVoteOrder.CPUB
		)
		self.v.save()

	def test_coalition_set(self):
		"""
		Test the line is defined
		"""
		self.g.resolve_current_turn()

		dinc_vote_session = self.g.dincvotesession_set.get(turn=self.g.current_turn)
		self.assertEqual(dinc_vote_session.coalition, self.v.coalition)

	def test_equality_no_coalition(self):
		"""
		When an equality occurs, no line is set
		"""
		self.v2 = DIncVoteOrder(
			player=self.p2,
			coalition=DIncVoteOrder.RSEC
		)
		self.v2.save()

		self.g.resolve_current_turn()

		dinc_vote_session = (self.g.dincvotesession_set.get(turn=self.g.current_turn))
		self.assertEqual(dinc_vote_session.coalition, None)
