from engine.models import Player
from engine.testcases import EngineTestCase
from engine_modules.mdc.models import MDCVoteOrder
from engine_modules.share.models import Share
from engine_modules.corporation.models import Corporation

class OrdersTest(EngineTestCase):
	def setUp(self):
		
		super(OrdersTest, self).setUp()

		self.p.money = 1000000
		self.p.save()

		self.p2 = Player(game=self.g, money=1000000)
		self.p2.save()

		self.g.corporation_set.all().delete()
		self.c = Corporation(base_corporation_slug='renraku', assets=20)
		self.g.corporation_set.add(self.c)
		self.c.share_set.all().delete()
		self.c2 = Corporation(base_corporation_slug='shiawase', assets=10)
		self.g.corporation_set.add(self.c2)
		self.c2.share_set.all().delete()

		self.s1 = Share(
			corporation=self.c,
			player=self.p,
			turn=self.g.current_turn
		)
		self.s1.save()

		self.s2 = Share(
			corporation=self.c,
			player=self.p,
			turn=self.g.current_turn
		)
		self.s2.save()

		self.v = MDCVoteOrder(
			player=self.p,
			party_line = MDCVoteOrder.MDC_PARTY_LINE_CHOICES[2][0]
		)
		self.v.save()

	def test_one_top_holder(self):
		"""
		Test that a top holder's vote is correctly weighed
		"""

		self.g.resolve_current_turn()
		self.assertEqual(self.reload(self.v).weight, 2)

	def test_no_top_holder(self):
		"""
		Test the case where no one holds any shares
		"""

		self.s1.delete()
		self.s2.delete()
		self.g.resolve_current_turn()
		self.assertEqual(self.reload(self.v).weight, 1)

	def test_equality_case(self):
		"""
		Test when two players have the same amount of shares
		"""

		self.s2.delete()
		self.s2 = Share(
			corporation=self.c,
			player=self.p2,
			turn=self.g.current_turn
		)
		self.s2.save()
		self.g.resolve_current_turn()
		
		self.assertEqual(self.reload(self.v).weight, 1)

	def test_top_holder_two_corporations(self):
		"""
		Test when a player is the top holder in two corporations
		"""
		
		self.s2.delete()
		self.s2 = Share(
			corporation=self.c2,
			player=self.p,
			turn=self.g.current_turn
		)
		self.s2.save()
		self.g.resolve_current_turn()
		
		self.assertEqual(self.reload(self.v).weight, 3)

