from engine.models import Player
from engine.testcases import EngineTestCase
from engine_modules.mdc.models import MDCVoteOrder
from engine_modules.share.models import Share
from engine_modules.corporation.models import Corporation


class OrdersTest(EngineTestCase):
	def setUp(self):
		
		super(OrdersTest, self).setUp()

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

	def not_top_holder(self):
		"""
		Test that your vote counts for 1 when you're not top holder
		"""
		self.assertEqual(self.reload(self.v).get_weight(), 1)

	def test_one_top_holder(self):
		"""
		Test that a top holder's vote is correctly weighed
		"""
		s = Share(
			corporation=self.c,
			player=self.p,
			turn=self.g.current_turn
		)
		s.save()

		self.assertEqual(self.reload(self.v).get_weight(), 2)

	def test_equality_case(self):
		"""
		Test when two players have the same amount of shares
		"""
		s = Share(
			corporation=self.c,
			player=self.p,
		)
		s.save()

		p2 = Player(game=self.g)
		p2.save()

		s2 = Share(
			corporation=self.c,
			player=p2,
		)
		s2.save()
	
		self.assertEqual(self.reload(self.v).get_weight(), 1)

	def test_top_holder_two_corporations(self):
		"""
		Test when a player is the top holder in two corporations
		"""
		s = Share(
			corporation=self.c,
			player=self.p,
		)
		s.save()

		s2 = Share(
			corporation=self.c2,
			player=self.p,
		)
		s2.save()
				
		self.assertEqual(self.reload(self.v).get_weight(), 3)
