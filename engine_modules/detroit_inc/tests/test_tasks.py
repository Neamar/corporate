# -*- coding: utf-8 -*-
from engine.models import Player
from engine.testcases import EngineTestCase
from engine_modules.share.models import Share
from engine_modules.detroit_inc.models import DIncVoteOrder
from messaging.models import Newsfeed


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

	def test_coalition_resolution_message(self):
		"""
		Beneficiary and victims get a note in resolution message
		"""
		v2 = DIncVoteOrder(
			player=self.p2,
			coalition=DIncVoteOrder.RSEC
		)
		v2.save()

		# Give priority to player 1
		Share(corporation=self.c, player=self.p, turn=self.g.current_turn).save()

		self.g.resolve_current_turn()

		self.assertIn("Detroit, Inc. a suivi", self.p.message_set.get().content)
		self.assertIn(u"Detroit, Inc. a rejoint la coalition opposée", self.p2.message_set.get().content)

	def test_coalition_newsfeed(self):
		"""
		Newsfeeds describes everything.
		"""
		self.p.name = "p1"
		self.p.save()
		self.p2.name = "p2"
		self.p2.save()

		v2 = DIncVoteOrder(
			player=self.p2,
			coalition=DIncVoteOrder.RSEC
		)
		v2.save()

		# Give priority to player 1
		s = Share(corporation=self.c, player=self.p, turn=self.g.current_turn)
		s.save()
		s2 = Share(corporation=self.c2, player=self.p, turn=self.g.current_turn)
		s2.save()

		self.g.resolve_current_turn()

		ns = Newsfeed.objects.last().content
		self.assertIn(self.p.name, ns)
		self.assertIn(self.p2.name, ns)
		self.assertIn(s.corporation.base_corporation.name, ns)
		self.assertIn(s2.corporation.base_corporation.name, ns)
		self.assertIn(self.v.get_coalition_display(), ns)
		self.assertIn(v2.get_coalition_display(), ns)
		self.assertIn("3 voix", ns)
		self.assertIn("1 voix", ns)
