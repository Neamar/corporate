# -*- coding: utf-8 -*-
from engine.models import Player
from engine.testcases import EngineTestCase
from engine_modules.share.models import Share
from engine_modules.mdc.models import MDCVoteOrder
from messaging.models import Newsfeed


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

	def test_coalition_resolution_message(self):
		"""
		Beneficiary and victims get a note in resolution message
		"""
		v2 = MDCVoteOrder(
			player=self.p2,
			coalition=MDCVoteOrder.BANK
		)
		v2.save()

		# Give priority to player 1
		Share(corporation=self.c, player=self.p, turn=self.g.current_turn).save()

		self.g.resolve_current_turn()

		self.assertIn("MDC a suivi", self.p.message_set.get().content)
		self.assertIn(u"MDC a rejoint la coalition opposée", self.p2.message_set.get().content)
