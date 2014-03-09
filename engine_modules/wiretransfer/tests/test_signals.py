from engine.testcases import EngineTestCase
from engine.exceptions import OrderNotAvailable
from engine_modules.wiretransfer.models import WiretransferOrder


class ModelTest(EngineTestCase):

	def test_wiretransfer_run_cant_send_to_self(self):
		"""
		Check you can't send money to yourself
		"""
		o = WiretransferOrder(
			player=self.p,
			recipient=self.p,
		)
		self.assertRaises(OrderNotAvailable, o.clean)
