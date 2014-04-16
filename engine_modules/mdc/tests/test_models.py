from engine.testcases import EngineTestCase
from engine_modules.mdc.models import MDCVoteOrder


class ModelsTest(EngineTestCase):
	def setUp(self):
		super(ModelsTest, self).setUp()

		self.v = MDCVoteOrder(
			player=self.p,
			coalition=MDCVoteOrder.DERE
		)
		self.v.clean()
		self.v.save()

	def test_player_get_last_mdc_vote(self):
		"""
		Get last mdc vote should return vote order
		"""

		self.assertIsNone(self.p.get_last_mdc_vote())
		self.g.resolve_current_turn()
		self.assertEqual(self.v, self.p.get_last_mdc_vote())

	def test_player_get_last_mdc_coalition(self):
		"""
		Get last mdc coalition should return coalition
		"""
		self.assertIsNone(self.p.get_last_mdc_coalition())
		self.g.resolve_current_turn()
		self.assertEqual(self.v.coalition, self.p.get_last_mdc_coalition())

	def test_game_get_mdc_coalition(self):
		"""
		Get mdc coalition should return coalition from specified turn
		"""
		self.g.resolve_current_turn()
		self.g.resolve_current_turn()
		self.assertIsNone(self.g.get_mdc_coalition())
		self.assertEqual(self.g.get_mdc_coalition(turn=self.g.current_turn - 1), self.v.coalition)
