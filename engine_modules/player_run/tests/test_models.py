from engine.testcases import EngineTestCase
from engine.exceptions import OrderNotAvailable
from engine_modules.player_run.models import InformationOrder


class ModelsTest(EngineTestCase):

	def test_information_run_cant_target_self(self):
		"""
		Check a Johnson can't target himself
		"""
		o = InformationOrder(
			target=self.p,
			player=self.p,
		)
		self.assertRaises(OrderNotAvailable, o.clean)
