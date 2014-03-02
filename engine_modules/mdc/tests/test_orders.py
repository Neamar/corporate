from engine.models import Player
from engine.testcases import EngineTestCase
from engine_modules.share.models import Share
from engine_modules.mdc.models import MDCVoteOrder


class OrdersTest(EngineTestCase):
	def setUp(self):
		super(OrdersTest, self).setUp()

		self.v = MDCVoteOrder(
			player=self.p,
			party_line=MDCVoteOrder.DERE
		)
		self.v.save()

	def test_not_top_holder(self):
		"""
		Test that your vote counts for 1 when you're not top holder
		"""
		self.assertEqual(self.v.get_weight(), 1)
		self.assertEqual(self.v.get_friendly_corporations(), [])

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

		self.assertEqual(self.v.get_weight(), 2)
		self.assertEqual(self.v.get_friendly_corporations(), [self.c])

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

		self.assertEqual(self.v.get_weight(), 1)

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

		self.assertEqual(self.v.get_weight(), 3)
		self.assertItemsEqual(self.v.get_friendly_corporations(), [self.c, self.c2])

	def test_mdc_party_line(self):
		"""
		Check party line is returned correctly
		"""
		self.assertIsNone(self.g.get_mdc_party_line())

		self.g.resolve_current_turn()

		self.assertEqual(self.g.get_mdc_party_line(), self.v.party_line)

	def test_get_last_mdv_vote(self):
		"""
		Check player last vote is returned correctly
		"""
		self.assertIsNone(self.p.get_last_mdc_vote())

		self.g.resolve_current_turn()

		self.assertEqual(self.p.get_last_mdc_vote(), self.v.party_line)
