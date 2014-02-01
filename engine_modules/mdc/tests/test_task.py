from random import randint

from engine.models import Player
from engine.testcases import EngineTestCase
from engine_modules.mdc.models import MDCVoteOrder, MDC_Party_Lines
from engine_modules.share.models import BuyShareOrder
from engine_modules.corporation.models import Corporation

class TaskTest(EngineTestCase):
	def setUp(self):
		
		super(TaskTest, self).setUp()

		self.p.money = 1000000
		self.p.save()

		self.p2 = Player(game=self.g, money=1000000)
		self.p2.save()

		self.p.order_set.all().delete()
		self.g.corporation_set.all().delete()
		self.c = Corporation(base_corporation_slug='renraku', assets=20)
		self.g.corporation_set.add(self.c)
		self.c.share_set.all().delete()
		self.c2 = Corporation(base_corporation_slug='shiawase', assets=10)
		self.g.corporation_set.add(self.c2)
		self.c2.share_set.all().delete()

		self.o1 = BuyShareOrder(
			player=self.p,
			corporation=self.c
		)
		self.o1.save()

		self.o2 = BuyShareOrder(
			player=self.p,
			corporation=self.c
		)
		self.o2.save()

		i = randint(0, len(MDC_Party_Lines.keys())-1)
		self.v = MDCVoteOrder(
			player=self.p,
			party_line = MDC_Party_Lines.keys()[i]
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

		self.o1.delete()
		self.o2.delete()
		self.g.resolve_current_turn()
		self.assertEqual(self.reload(self.v).weight, 1)

	def test_equality_case(self):
		"""
		Test when two players have the same amount of shares
		"""

		self.o2.player = self.p2
		self.o2.save()
		self.g.resolve_current_turn()
		
		self.assertEqual(self.reload(self.v).weight, 1)

	def test_top_holder_two_corporations(self):
		"""
		Test when a player is the top holder in two corporations
		"""
		
		self.o2.corporation = self.c2
		self.o2.save()
		self.g.resolve_current_turn()
		
		self.assertEqual(self.reload(self.v).weight, 3)

	def test_party_line_set(self):

		self.g.resolve_current_turn()
		line = (self.g.mdcvotesession_set.filter(turn=self.g.current_turn)[0]).current_party_line
		self.assertEqual(line, self.v.party_line)

	def test_equality_no_party_line(self):
	
		self.v.party_line = "cpublics"
		self.v2 = MDCVoteOrder(
			player=self.p,
			party_line = "transparence"
		)
		self.v2.save()
		self.g.resolve_current_turn()

		line = (self.g.mdcvotesession_set.filter(turn=self.g.current_turn)[0]).current_party_line
		self.assertEqual(line, "aucune")
