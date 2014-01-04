from engine.testcases import EngineTestCase
from engine_modules.player_run.models import InformationRunOrder
from engine.exceptions import OrderNotAvailable


class TaskTest(EngineTestCase):
	"""
	Unit tests for Player's runs
	"""

	def test_information_run_cant_target_self(self):
		"""
		Check if a Johnson can't target himself
		"""
		o = InformationRunOrder(
			target=self.p,
			player=self.p,
		)
		self.assertRaises(OrderNotAvailable, o.save)
