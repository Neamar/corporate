from engine.testcases import EngineTestCase
from engine_modules.detroit_inc.models import DIncVoteOrder


class ModelsTest(EngineTestCase):
	def setUp(self):
		super(ModelsTest, self).setUp()

		self.v = DIncVoteOrder(
			player=self.p,
			coalition=DIncVoteOrder.CPUB
		)
		self.v.clean()
		self.v.save()

	def test_player_get_last_dinc_vote(self):
		"""
		get_last_dinc_vote should return vote order
		"""

		self.assertIsNone(self.p.get_last_dinc_vote())
		self.g.resolve_current_turn()
		self.assertEqual(self.v, self.p.get_last_dinc_vote())

	def test_player_get_last_dinc_coalition(self):
		"""
		get_last_dinc_coalition should return coalition
		"""
		self.assertIsNone(self.p.get_last_dinc_coalition())
		self.g.resolve_current_turn()
		self.assertEqual(self.v.coalition, self.p.get_last_dinc_coalition())

	def test_game_get_dinc_coalition(self):
		"""
		get_dinc_coalition should return coalition from specified turn
		"""
		self.g.resolve_current_turn()
		self.g.resolve_current_turn()
		self.assertIsNone(self.g.get_dinc_coalition())
		self.assertEqual(self.g.get_dinc_coalition(turn=self.g.current_turn - 1), self.v.coalition)
