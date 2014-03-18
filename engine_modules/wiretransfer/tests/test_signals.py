from engine.testcases import EngineTestCase
from engine.exceptions import OrderNotAvailable
from engine_modules.wiretransfer.models import WiretransferOrder
from engine.models import Player


class SignalsTest(EngineTestCase):
	def test_wiretransfer_run_cant_send_to_self(self):
		"""
		Check you can't send money to yourself
		"""
		o = WiretransferOrder(
			player=self.p,
			recipient=self.p,
			amount=1
		)
		self.assertRaises(OrderNotAvailable, o.clean)

	def test_wiretransfer_run_cant_send_more_than_available(self):
		"""
		Check you can't send more money than you have right now
		"""
		p2 = Player(game=self.g)
		p2.save()

		o = WiretransferOrder(
			player=self.p,
			recipient=p2,
			amount=self.p.money + 1
		)
		self.assertRaises(OrderNotAvailable, o.clean)
